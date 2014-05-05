#!/bin/bash
set -e # exit on error

# setup the snapable api code
if [ ! -f ~/api_bootstrap ]; then
    echo ""
    echo "+----------------+"
    echo "| Setup Snapable |"
    echo "+----------------+"
    echo ""
    # run the setup instruction commands for the api
    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py syncdb'
    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py migrate api'
    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py migrate data'

    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py loaddata ~/snap_api/api/data/fixtures/packages.json'

    touch ~/api_bootstrap
else
    echo ""
    echo "+-----------------+"
    echo "| Update Snapable |"
    echo "+-----------------+"
    echo ""
    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py syncdb'
    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py migrate api'
    su - vagrant -c '~/snap_api/bin/python ~/snap_api/api/manage.py migrate data'
fi