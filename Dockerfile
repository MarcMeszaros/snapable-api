FROM        ubuntu:trusty
MAINTAINER  Marc Meszaros <marc@snapable.com>

# install dependencies
RUN apt-get update && apt-get -y install \
    git \
    make \
    nginx \
    ntp \
    python \
    python-apt \
    python-dev \
    python-pip \
    python3 \
    python3-dev \
    libffi-dev \
    libfreetype6-dev \
    libjpeg8-dev \
    liblcms1-dev \
    libmysqlclient-dev \
    libtiff4-dev \ 
    libwebp-dev \
    supervisor \
    zlib1g-dev \
    && pip install virtualenv \
    && rm -rf /var/lib/apt/lists/*

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
COPY hooks /src/app/hooks/
COPY utils /src/app/utils/
COPY worker /src/app/worker/

# static files
RUN cd /src/app && /src/bin/python ./manage.py collectstatic --noinput
COPY static-www /src/html/static-www/
COPY docs/build/html /src/html/docs/

# running
ENV NEW_RELIC_CONFIG_FILE /src/app/newrelic.ini
ENV NEW_RELIC_ENVIRONMENT staging

EXPOSE 80
EXPOSE 8000
WORKDIR /src/app

CMD ["supervisord", "-n"]
#CMD ["/src/bin/gunicorn", "wsgi:application", "--pid gunicorn.pid"]
#CMD ["/src/bin/newrelic-admin", "run-program", "/src/bin/gunicorn", "wsgi:application", "--pid gunicorn.pid"]