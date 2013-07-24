#!/usr/bin/env bash

# update the vm (first run only)
if [ ! -f ~/vagrant_worker_bootstrap ]; then
    echo ""
    echo "+-------------------+"
    echo "| Update the System |"
    echo "+-------------------+"
    echo ""
    #apt-get -y upgrade
    # include extra dependecies
    pip install supervisor virtualenv
fi

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
# setup supervisor
su - vagrant -c 'cp -f /vagrant/script/vagrant_snap_worker.conf ~/supervisor/snap_worker.conf'
su - vagrant -c 'supervisorctl update'

# touch a file to know that the setup is done
touch ~/vagrant_worker_bootstrap