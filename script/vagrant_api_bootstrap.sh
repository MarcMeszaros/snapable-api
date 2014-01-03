#!/usr/bin/env bash

# setup the snapable api code
echo ""
echo "+----------------+"
echo "| Setup Snapable |"
echo "+----------------+"
echo ""
# run the setup instruction commands for the api
su - vagrant -c '~/api/bin/pip install -v -r ~/api/snapable/requirements.txt'
su - vagrant -c '~/api/bin/python ~/api/snapable/manage.py syncdb'
su - vagrant -c '~/api/bin/python ~/api/snapable/manage.py migrate data'
su - vagrant -c '~/api/bin/python ~/api/snapable/manage.py migrate api'

if [ -f ~/vagrant_api_bootstrap ]; then
    su - vagrant -c '~/api/bin/python ~/api/snapable/manage.py loaddata ~/api/snapable/data/fixtures/packages.json'
fi

# touch a file to know that the setup is done
touch ~/vagrant_api_bootstrap