#!/usr/bin/env bash

if [ ! -f /etc/apt/sources.list.d/rabbitmq.list ]; then
    echo "deb http://www.rabbitmq.com/debian/ testing main" > /etc/apt/sources.list.d/rabbitmq.list
    wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
    apt-key add rabbitmq-signing-key-public.asc
    rm rabbitmq-signing-key-public.asc
fi

# install packages
echo ""
echo "+-------------------------+"
echo "| Install System Packages |"
echo "+-------------------------+"
echo ""
apt-get update
apt-get -y install ntp git make python-dev python-pip libevent-dev libmysqlclient-dev libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms1-dev libwebp-dev 
apt-get -y install rabbitmq-server
