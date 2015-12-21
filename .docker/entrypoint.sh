#!/bin/sh
set -e

start_api () {
  # start nginx in daemon mode
  nginx

  # start gunicorn
  /src/bin/newrelic-admin run-program /src/bin/gunicorn wsgi:application --pid gunicorn.pid
}

start_worker () {
  /src/bin/celery worker -A worker -l info
}

start_beat () {
  /src/bin/celery beat -A worker -l info
}

help () {
  echo 'entrypoint.sh {api,worker,beat}'
}

# start the correct application
if [ "$1" = "api" ]; then
  start_api
elif [ "$1" = "worker" ]; then
  start_worker
elif [ "$1" = "beat" ]; then
  start_beat
else
  help
fi
