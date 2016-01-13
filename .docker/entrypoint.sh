#!/bin/sh
set -e

start_api () {
  # start nginx in daemon mode
  nginx

  # start gunicorn
  /src/bin/newrelic-admin run-program /src/bin/gunicorn wsgi:application
}

start_worker () {
  /src/bin/celery worker -A worker -l info
}

start_beat () {
  /src/bin/celery beat -A worker -l info
}

migrate () {
  # run migrations
  /src/bin/python manage.py migrate
}

test () {
  /src/bin/python manage.py test
}

shell () {
  /src/bin/python manage.py shell
}

help () {
  echo 'entrypoint.sh {api,worker,beat,shell} [migrate]'
}

#run migrations if the extra param is appended
if [ "$2" = "migrate" ]; then
  migrate
fi

# start the correct application
if [ "$1" = "api" ]; then
  start_api
elif [ "$1" = "worker" ]; then
  start_worker
elif [ "$1" = "beat" ]; then
  start_beat
elif [ "$1" = "test" ]; then
  test
elif [ "$1" = "shell" ]; then
  shell
else
  help
fi
