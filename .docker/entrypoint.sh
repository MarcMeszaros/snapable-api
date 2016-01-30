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

bash () {
  /bin/bash
}

help () {
  echo "NAME:"
  echo "\t entrypoint.sh - A wrapper script for starting the application."
  echo ""
  echo "USAGE:"
  echo "\t entrypoint.sh {api,worker,beat,test,shell,bash} [migrate]"
  echo ""
  echo "POSITIONAL ARGUMENTS:"
  echo "\t api \t\t Run the api process"
  echo "\t worker \t Start the worker"
  echo "\t beat \t\t Start a celery beat"
  echo "\t test \t\t Run the test suite"
  echo "\t shell \t\t Start a Django shell"
  echo "\t bash \t\t Start a bash shell"
  echo ""
  echo "OPTIONAL POSITIONAL ARGUMENTS:"
  echo "\t migrate \t Run Django migration before the positional argument"
  echo ""
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
elif [ "$1" = "bash" ]; then
  bash
else
  help
fi
