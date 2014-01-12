#!/usr/bin/env bash

# setup the snapable api code
echo ""
echo "+----------------+"
echo "| Setup Snapable |"
echo "+----------------+"
echo ""
# run the setup instruction commands for the api
su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py syncdb'
su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py migrate data'
su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py migrate api'

if [ -f ~/vagrant_api_bootstrap ]; then
    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py loaddata ~/snap_api/api/data/fixtures/packages.json'
fi

# touch a file to know that the setup is done
touch ~/vagrant_api_bootstrap