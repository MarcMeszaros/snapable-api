#!/bin/sh

# generate the docs
(cd docs && make html)

# build the new docker image
docker build .