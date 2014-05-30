#!/bin/bash

dpkg-query -l mysql-server > /dev/null 2>&1
INSTALLED=$?
if [ $INSTALLED != '0' ]; then
    echo ""
    echo "+-------------+"
    echo "| Setup MySQL |"
    echo "+-------------+"
    echo ""
    debconf-set-selections <<< "mysql-server-5.5 mysql-server/root_password password snapable12345"
    debconf-set-selections <<< "mysql-server-5.5 mysql-server/root_password_again password snapable12345"
    apt-get -y install mysql-server
    mysql -u root --password=snapable12345 -e "CREATE USER 'snapableusr'@'localhost' IDENTIFIED BY 'snapable12345';"
    mysql -u root --password=snapable12345 -e "CREATE DATABASE snapabledb;"
    mysql -u root --password=snapable12345 -e "GRANT ALL PRIVILEGES ON *.* to snapableusr@'192.168.56.%' IDENTIFIED BY 'snapable12345';"

    # add custom tweaks to config file
    sed -i "s/127\.0\.0\.1/0\.0\.0\.0/" /etc/mysql/my.cnf
    service mysql restart
fi