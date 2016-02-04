FROM debian:8.3
MAINTAINER Marc Meszaros <marc@snapable.com>

# install dependencies
RUN apt-get update && apt-get -y install \
    build-essential \
    curl \
    make \
    nginx \
    ntp \
    python \
    python-dev \
    python3 \
    python3-dev \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libmysqlclient-dev \
    libwebp-dev \
    zlib1g-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install pip (and sphinx for docs)
RUN curl -sL https://bootstrap.pypa.io/get-pip.py | python - \
    && pip install virtualenv sphinx

# install nodejs (and aglio for docs)
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g aglio

# virtualenv
RUN virtualenv /src && mkdir -p /src/html

# static files & docs
COPY docs /src/docs
RUN cd /src/docs \
  && make html \
  && mv /src/docs/build/html /src/html/docs/

# requirements
COPY app/requirements.txt /tmp/requirements.txt
RUN /src/bin/pip install -r /tmp/requirements.txt

# app code
COPY app /src/app/
WORKDIR /src/app
RUN /src/bin/python manage.py collectstatic --noinput \
  && mv /src/app/static-www /src/html/static-www/

# running
ENV NEW_RELIC_CONFIG_FILE /src/app/newrelic.ini
ENV NEW_RELIC_ENVIRONMENT staging

# nginx
# change back to root for nginx config and running the app
RUN useradd -ms /bin/bash nginx
COPY .docker/nginx.conf /etc/nginx/nginx.conf

# running
ENV C_FORCE_ROOT true
EXPOSE 80 8000
COPY .docker/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["api"]
