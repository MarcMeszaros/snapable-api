#!/usr/bin/env bash

if [ ! -f ~/salt_dependencies ]; then
    echo ""
    echo "+-------------------------+"
    echo "| Setup Salt Dependencies |"
    echo "+-------------------------+"
    echo ""
    apt-get update -qq
    apt-get -y install python-git

    touch ~/salt_dependencies
fi

if [ ! -f ~/salt_hosts ]; then
    echo ""
    echo "+-----------------+"
    echo "| Add Known Hosts |"
    echo "+-----------------+"
    echo ""
    mkdir -p /root/.ssh
    cat /vagrant/salt/key/known_hosts >> /root/.ssh/known_hosts
    cp /vagrant/salt/key/id_deployment /root/.ssh/id_rsa
    cp /vagrant/salt/key/id_deployment.pub /root/.ssh/id_rsa.pub
    chmod 0600 /root/.ssh/id_rsa

    touch ~/salt_hosts
fi