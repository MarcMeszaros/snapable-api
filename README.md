# INTRODUCTION #
This is the main API code used for Snapable.

# REQUIREMENTS #
Development is done on Ubuntu 12.04 LTS systems (http://www.ubuntu.com/).
You can view the library versions developed against in the "requirements.txt" file.
To install all the libraries at once using pip (http://www.pip-installer.org/).

The following are the minimum system requirements:

* python 2.7+ (http://www.python.org/)
* ntp 
* git 
* make
* python-dev
* python-pip
* libjpeg-dev
* libwebp-dev
* libevent-dev
* libmysqlclient-dev

# INSTALLATION #

## Production Install ##
The installation assumes that the following steps are executed on a server that meets the requirements.
The application is set to use the following MySQL credentials by default:

    host: localhost
    user: root
    pass: snapable12345
    db: snapabledb

1. Get the source code.
2. Setup the migration management via south/django and the "syncdb" command.
3. Apply the database migrations.
4. Simply run the application using wsgi. Using gunicorn (http://gunicorn.org/) is recommended.

## Development Install ##

1. Complete the "Production Install"
2. Run `pip install -r requirements-dev.txt`

## MANUAL INSTALLATION EXAMPLE: ##
Run the following commands:

    > sudo apt-get install build-essential python python-dev python-pip libmysqlclient-dev libjpeg-dev libevent-dev
    > sudo pip install --upgrade
    > sudo pip install virtualenv
    > mkdir ~/environments/
    > virtualenv ~/environments/api/
    > cd ~/environments/api/
    > git clone git@bitbucket.org:snapable/api.git snapable
    > source bin/activate
    > cd snapable
    > pip install -r requirements.txt
    > ./manage.py syncdb
    > ./manage.py migrate data
    > ./manage.py migrate api
    > gunicorn api.wsgi:application -c gunicorn.conf.py

# DEVELOPMENT #

## Unit Tests ##
To run the unit tests, execute:

    ./manage.py test

# CONFIGURATION #
Below is a sample configuration for the local settings file. It should be placed 
in the root API source code folder.

    import os

    # set some environment variables
    os.environ['RACKSPACE_SERVICENET'] = '1' # makes 'python-cloudfiles' use ServiceNet which doesn't cost data transfer usage

    # database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'my_db',                 # Or path to database file if using sqlite3.
            'USER': 'my_user',               # Not used with sqlite3.
            'PASSWORD': 'my_pass',           # Not used with sqlite3.
            'HOST': 'my_host',               # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

    # sendgrid
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'my_user' # only save in local settings
    EMAIL_HOST_PASSWORD = 'my_pass' # only save in local settings
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    # RACKSPACE
    RACKSPACE_USERNAME = 'my_user'
    RACKSPACE_APIKEY = 'my_api_key'
    RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = 'dev_images_'

    # sentry/raven
    SENTRY_DSN = 'http://user:pass@host/2'

    # API keys
    APIKEY = {
        'abc123': '123', # production testing key/secret pair
    }