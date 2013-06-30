#!/usr/bin/env bash

# update the vm
echo ""
echo "+-------------------+"
echo "| Update the System |"
echo "+-------------------+"
echo ""
#apt-get -y upgrade
# include extra dependecies
pip install supervisor virtualenv

# setup the supervisor configs
if [ ! -f /etc/supervisord.conf ]; then
    echo ""
    echo "+------------------+"
    echo "| Setup Supervisor |"
    echo "+------------------+"
    echo ""
    echo_supervisord_conf > /etc/supervisord.conf
    cat /vagrant/script/supervisord > /etc/init.d/supervisord
    # add custom tweaks to config file
    sed -i 's/;chmod=0700/chmod=0764/' /etc/supervisord.conf
    sed -i 's/;chown=nobody:nogroup/chown=root:vagrant/' /etc/supervisord.conf
    sed -i 's/;\[include\]/\[include\]/' /etc/supervisord.conf
    echo "files = /home/vagrant/supervisor/*.conf" >> /etc/supervisord.conf
    su - vagrant -c 'mkdir ~/supervisor'
    # start supervisor on boot
    chmod +x /etc/init.d/supervisord
    update-rc.d supervisord defaults
    service supervisord start
fi

# setup the mysql
dpkg-query -l mysql-server > /dev/null 2>&1
INSTALLED=$?
if [ $INSTALLED != '0' ]; then
    echo ""
    echo "+-------------+"
    echo "| Setup MySQL |"
    echo "+-------------+"
    echo ""
    debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password snapable12345'
    debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password snapable12345'
    apt-get -y install mysql-server
    mysql -u root --password=snapable12345 -e 'CREATE DATABASE snapabledb;'
    mysql -u root --password=snapable12345 -e 'GRANT ALL PRIVILEGES ON snapabledb.* to root@localhost;'
fi

# setup the snapable api code
echo ""
echo "+----------------+"
echo "| Setup Snapable |"
echo "+----------------+"
echo ""
# setup the virtualenv
if [ ! -d /home/vagrant/environments ]; then
    su - vagrant -c 'mkdir ~/environments'
    su - vagrant -c 'virtualenv -q ~/environments/api'
    su - vagrant -c 'ln -s /vagrant ~/environments/api/snapable'
fi
# run the setup instruction commands for the api
su - vagrant -c '~/environments/api/bin/pip install -v -r /vagrant/requirements.txt'
su - vagrant -c '~/environments/api/bin/pip install -v -r /vagrant/requirements-dev.txt'
su - vagrant -c '~/environments/api/bin/python ~/environments/api/snapable/manage.py syncdb'
su - vagrant -c '~/environments/api/bin/python ~/environments/api/snapable/manage.py migrate data'
su - vagrant -c '~/environments/api/bin/python ~/environments/api/snapable/manage.py migrate api'
# setup supervisor
su - vagrant -c 'cp -f /vagrant/script/vagrant_snap_api.conf ~/supervisor/snap_api.conf'
su - vagrant -c 'supervisorctl update'