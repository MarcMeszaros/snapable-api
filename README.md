# INTRODUCTION #
This is the main API code used for Snapable.

# REQUIREMENTS #
Development is done on [Ubuntu 12.04 LTS](http://www.ubuntu.com/).
You can view the library versions developed against in the "requirements.txt" file.
To install all the libraries at once using [pip](http://www.pip-installer.org/).

## System Requirements ##
System packages required are for the pip installer to work:

* git (generic)
* make (generic)
* python-dev (generic)
* libffi-dev (bcrypt)
* libtiff4-dev  (pillow)
* libjpeg8-dev (pillow)
* zlib1g-dev (pillow)
* libfreetype6-dev (pillow)
* liblcms1-dev (pillow)
* libwebp-dev (pillow)

## MANUAL INSTALLATION EXAMPLE ##
Run the following commands:

    > sudo pip install --upgrade
    > sudo pip install virtualenv
    > virtualenv ~/snap_api/
    > cd ~/snap_api/
    > source bin/activate
    > git clone git@bitbucket.org:snapable/api.git
    > cd api
    > pip install -r requirements.txt
    > ./manage.py syncdb
    > ./manage.py migrate data
    > ./manage.py migrate api
    > gunicorn wsgi:application

# DEVELOPMENT #

## Development Install ##

You need to have [VirtualBox](https://www.virtualbox.org/) installed and [Vagrant](http://www.vagrantup.com/).

1. Run ``vagrant up`` in the root folder, then go have a coffee (this may take a while the first time).
2. Run ``vagrant ssh`` to connect to the VM

### Disable Authentication Check ###
It can be annoying to develop on the API and have to build a client that conforms to the request
signing requirements of the API. Thankfully, you can disable the authentication checks by starting up
the server with the ``SNAP_AUTHENTICATION`` environment variable set to ``False``. Gunicorn has a special
option to pass in environment variables to your application.

``gunicorn -e SNAP_AUTHENTICATION=False wsgi:application``

## Unit Tests ##
To run the unit tests, you first need to log on to the VM using ``vagrant ssh``. Then execute the following commands:

    cd ~/snap_api
    source bin/activate
    cd api
    ./manage.py test

# CONFIGURATION #
Below is a sample configuration for the local settings file. It should be placed 
in the root API source code folder.

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

    # mailgun
    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_HOST_USER = 'my_user' # only save in local settings
    EMAIL_HOST_PASSWORD = 'my_pass' # only save in local settings

    # RACKSPACE
    RACKSPACE_USERNAME = 'my_user'
    RACKSPACE_APIKEY = 'my_api_key'
    RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = 'mydev_images_'
    RACKSPACE_CLOUDFILE_PUBLIC_NETWORK = True

    # sentry/raven
    RAVEN_CONFIG = {
        'dsn': 'http://user:pass@host/2',
    }

    # API keys
    APIKEY = {
        'key123': 'sec123', # production testing key/secret pair
    }