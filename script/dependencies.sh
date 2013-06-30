#!/usr/bin/env bash

# install packages
echo ""
echo "+-------------------------+"
echo "| Install System Packages |"
echo "+-------------------------+"
echo ""
apt-get update
apt-get -y install ntp git make python-dev python-pip libjpeg-dev libwebp-dev libevent-dev libmysqlclient-dev
