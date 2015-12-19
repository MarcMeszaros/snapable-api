FROM ubuntu:15.04
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
    libjpeg8-dev \
    libmysqlclient-dev \
    libtiff5-dev \
    libwebp-dev \
    supervisor \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install pip (and sphinx for docs)
RUN curl -sL /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py | python - \
    && pip install virtualenv sphinx

# install nodejs (and aglio for docs)
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g aglio

# nginx
RUN useradd -ms /bin/bash nginx
COPY .docker/supervisor.conf /etc/supervisor/conf.d/
COPY .docker/nginx.conf /etc/nginx/nginx.conf

# virtualenv
RUN virtualenv /src && mkdir -p /src/html

# pip requirement
COPY requirements.txt /tmp/requirements.txt
RUN cd /tmp && /src/bin/pip install -r /tmp/requirements.txt

# static files & docs
COPY docs /src/docs
RUN cd /src/docs \
  && make html \
  && mv /src/docs/build/html /src/html/docs/

# app code
COPY app /src/app/
RUN cd /src/app \
  && /src/bin/python ./manage.py collectstatic --noinput \
  && mv /src/app/static-www /src/html/static-www/

# running
ENV NEW_RELIC_CONFIG_FILE /src/app/newrelic.ini
ENV NEW_RELIC_ENVIRONMENT staging

EXPOSE 80 8000
WORKDIR /src/app

CMD ["supervisord", "-n"]
#CMD ["/src/bin/gunicorn", "wsgi:application", "--pid gunicorn.pid"]
#CMD ["/src/bin/newrelic-admin", "run-program", "/src/bin/gunicorn", "wsgi:application", "--pid gunicorn.pid"]
