FROM ubuntu:14.10
MAINTAINER  Marc Meszaros <marc@snapable.com>

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
    libffi-dev \
    libfreetype6-dev \
    libjpeg8-dev \
    liblcms1-dev \
    libmysqlclient-dev \
    libtiff5-dev \ 
    libwebp-dev \
    supervisor \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# install pip (and sphinx for docs)
RUN curl -SL -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py \
    && python /tmp/get-pip.py \
    && pip install virtualenv sphinx

# install nodejs (and aglio for docs)
RUN curl -sL https://deb.nodesource.com/setup | bash - \
    && apt-get install -y nodejs \
    && npm install -g aglio

# nginx
RUN useradd -ms /bin/bash nginx
COPY .docker/supervisor.conf /etc/supervisor/conf.d/
COPY .docker/nginx.conf /etc/nginx/nginx.conf

# virtualenv
RUN virtualenv /src

# pip requirement
COPY requirements.txt /tmp/requirements.txt
RUN cd /tmp && /src/bin/pip install -r /tmp/requirements.txt

# app code
COPY *.py /src/app/
COPY *.ini /src/app/
COPY ajax /src/app/ajax/
COPY api /src/app/api/
COPY dashboard /src/app/dashboard/
COPY data /src/app/data/
COPY docs /src/app/docs
COPY hooks /src/app/hooks/
COPY utils /src/app/utils/
COPY worker /src/app/worker/

# static files & docs
RUN cd /src/app && /src/bin/python ./manage.py collectstatic --noinput
RUN cd /src/app/docs && make html
RUN mkdir -p /src/html \
    && mv /src/app/static-www /src/html/static-www/ \
    && mv /src/app/docs/build/html /src/html/docs/

# running
ENV NEW_RELIC_CONFIG_FILE /src/app/newrelic.ini
ENV NEW_RELIC_ENVIRONMENT staging

EXPOSE 80
EXPOSE 8000
WORKDIR /src/app

CMD ["supervisord", "-n"]
#CMD ["/src/bin/gunicorn", "wsgi:application", "--pid gunicorn.pid"]
#CMD ["/src/bin/newrelic-admin", "run-program", "/src/bin/gunicorn", "wsgi:application", "--pid gunicorn.pid"]