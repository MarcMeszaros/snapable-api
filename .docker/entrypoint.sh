#!/bin/sh
set -e

start_api () {
  # start nginx in daemon mode
  nginx

  # start gunicorn
  /src/bin/newrelic-admin run-program /src/bin/gunicorn wsgi:application
}

start_runserver () {
  exec /src/bin/python manage.py runserver 0.0.0.0:8000
}

start_worker () {
  exec /src/bin/celery worker -A worker -l info
}

start_beat () {
  exec /src/bin/celery beat -A worker -l info
}

migrate () {
  # run migrations
  /src/bin/python manage.py migrate
}

test () {
  exec /src/bin/python manage.py test
}

django_shell () {
  exec /src/bin/python manage.py shell
}

shell () {
  exec /bin/sh
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
  echo "\t runserver \t Run in development mode"
  echo "\t worker \t Start the worker"
  echo "\t beat \t\t Start a celery beat"
  echo "\t test \t\t Run the test suite"
  echo "\t django_shell \t Start a Django shell"
  echo "\t shell \t\t Start a system shell"
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
elif [ "$1" = "runserver" ]; then
  start_runserver
elif [ "$1" = "worker" ]; then
  start_worker
elif [ "$1" = "beat" ]; then
  start_beat
elif [ "$1" = "test" ]; then
  test
elif [ "$1" = "django_shell" ]; then
  django_shell
elif [ "$1" = "shell" ]; then
  shell
else
  help
fi
