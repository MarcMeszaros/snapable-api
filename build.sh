#!/bin/sh

# compile all the assets
./manage.py collectstatic --clear --noinput

# generate the docs
(cd docs && make html)

# build the new docker image
docker build .