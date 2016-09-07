FROM alpine:3.4
MAINTAINER Marc Meszaros <marc@snapable.com>

# install dependencies
RUN apk add --update \
    bash \
    bash-doc \
    bash-completion \
    build-base \
    ca-certificates \
    dbus-dev \
    dbus-glib-dev \
    git \
    jpeg-dev \
    linux-headers \
    nginx \
    nodejs \
    openssl \
    openssl-dev \
    python \
    python-dev \
    py-pip \
    zlib-dev \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

# create the user and application source directory & venv
RUN addgroup app && adduser -S app -G app \
  && mkdir /src && chown app:app /src \
  && mkdir -p /src/html \
  && virtualenv /src

# install sphinx and aglio (for docs)
RUN pip install sphinx \
  && npm install -g aglio

# static files & docs
COPY docs /src/docs
RUN cd /src/docs \
  && make html \
  && mv /src/docs/build/html /src/html/docs/

# requirements
COPY app/requirements.txt /tmp/requirements.txt
RUN CFLAGS="$CFLAGS -L/lib" /src/bin/pip install -r /tmp/requirements.txt

# app code
COPY app /src/app/
WORKDIR /src/app
RUN /src/bin/python manage.py collectstatic --noinput \
  && mv /src/app/static-www /src/html/static-www/

# running
ENV NEW_RELIC_CONFIG_FILE /src/app/newrelic.ini
ENV NEW_RELIC_ENVIRONMENT staging

# nginx
COPY .docker/nginx.conf /etc/nginx/nginx.conf

# running
ENV C_FORCE_ROOT true
EXPOSE 80 8000

COPY .docker/wait-for-it.sh /
RUN chmod +x /wait-for-it.sh
COPY .docker/entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
CMD ["api"]
