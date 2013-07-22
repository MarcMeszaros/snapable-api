#!/usr/bin/env bash

# install packages
echo ""
echo "+-------------------------+"
echo "| Install System Packages |"
echo "+-------------------------+"
echo ""
apt-get update
apt-get -y install ntp git make python-dev python-pip libevent-dev libmysqlclient-dev libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms1-dev libwebp-dev
