# INTRODUCTION #

This is the main API code used for Snapable.

# REQUIREMENTS #

Development is done on Debian 6.0.5 (a.k.a. Squeeze) systems (http://www.debian.org/).
You can view the library versions developed against in the "requirements.txt" file.
To install all the libraries at once using pip (http://www.pip-installer.org/).

The following are the minimum system requirements:

* *python 2.6+ (http://www.python.org/) Note: "python-dev" package required to install "Netifaces"
* *python-pip
* *libjpeg-dev
* *libraw-dev
* *libevent-dev
* *mysql-dev
* MySQLdb (http://sourceforge.net/projects/mysql-python)
* Django (https://www.djangoproject.com/)
* JSONField (https://github.com/bradjasper/django-jsonfield)
* South (https://bitbucket.org/andrewgodwin/south)
* Tastypie (https://github.com/toastdriven/django-tastypie)
* Netifaces (http://alastairs-place.net/projects/netifaces/)
* setproctitle (https://github.com/dvarrazzo/py-setproctitle)
* Rackspace Cloudfiles (https://github.com/rackspace/python-cloudfiles)
* Pillow (https://github.com/python-imaging/Pillow)

NOTE: * items are installed from the Debian distribution using APT.

# INSTALLATION #

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

## INSTALLATION EXAMPLE: ##
Run the following commands:

    > git clone git@bitbucket.org:snapable/api.git snapable
    > cd snapable
    > apt-get install build-essential python python-dev python-pip libjpeg-dev libraw-dev libevent-dev
    > pip install --upgrade
    > pip install -r requirements.txt
    > ./manage.py syncdb
    > ./manage.py migrate data
    > gunicorn api.wsgi:application -c gunicorn_config.py

Execute the following commands to control the server:

    # reload (note: ` [backticks] are required)
    kill -HUP `cat gunicorn.pid`

    # kill (note: ` [backticks] are required)
    kill -9 `cat gunicorn.pid`

# CONFIGURATION #

Below is a sample configuration for the local settings file. It should be placed one folder level
higher than the "snapable" API source code folder.

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

    # django settings
    DEBUG = True

    DEBUG_AUTHENTICATION = True
    DEBUG_AUTHORIZATION = True

    ADMINS = (
        ('Marc Meszaros', 'marc@snapable.com'),
        ('Andrew Draper', 'andrew@snapable.com'),
    )

    # sendgrid
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'my_user' # only save in local settings
    EMAIL_HOST_PASSWORD = 'my_pass' # only save in local settings
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    # RACKSPACE
    RACKSPACE_USERNAME = 'my_user'
    RACKSPACE_APIKEY = 'my_api_key'
    RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = 'dev_photos_'

    # sentry/raven
    SENTRY_DSN = 'http://user:pass@host/2'
    RAVEN_CONFIG = {
        'register_signals': True,
    }

    # API keys
    APIKEY = {
        'abc123': '123', # general testing key/secret pair
    }