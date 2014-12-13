# INTRODUCTION #
This is the main API code used for Snapable.

# REQUIREMENTS #
Development is done on [Ubuntu 14.04 LTS](http://www.ubuntu.com/).
You can view the library versions developed against in the "requirements.txt" file.
To install all the libraries at once using [pip](http://www.pip-installer.org/).

## System Requirements ##
System packages required are for the pip installer and some libraries to work:

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
    > ./manage.py migrate api
    > ./manage.py migrate data
    > gunicorn wsgi:application

# DEVELOPMENT #

## Development Install ##

You need to have [VirtualBox](https://www.virtualbox.org/) installed and [Vagrant](http://www.vagrantup.com/).

1. Run ``vagrant up`` in the root folder, then go have a coffee (this may take a while the first time - 15+ mins).
2. Run ``vagrant ssh`` to connect to the VM

### Disable Authentication Check ###
It can be annoying to develop on the API and have to build a client that conforms to the request
signing requirements of the API. Thankfully, you can disable the authentication checks by starting up
the server with the ``SNAP_AUTHENTICATION`` environment variable set to ``False``. Gunicorn has a special
option to pass in environment variables to your application.

``gunicorn -e SNAP_AUTHENTICATION=False wsgi:application``

## Docker ##
http://www.devopslife.com/2014/08/08/docker-boot2docker-and-dns-resolution-of-containers.html

1. ``docker pull mysql``
2. ``docker run --name db-mysql -e MYSQL_ROOT_PASSWORD="snapable12345" -e MYSQL_USER="snapableusr" -e MYSQL_PASSWORD="snapable12345" -e MYSQL_DATABASE="snapabledb" mysql``
``docker start -a db-mysql``
3. ``docker run -i -t --link db-mysql:db -p 8000:8000 <container ID>``

## Unit Tests ##
To run the unit tests, you first need to log on to the VM using ``vagrant ssh``. Then execute the following commands:

    cd ~/snap_api
    source bin/activate
    cd api
    ./manage.py test

# CONFIGURATION #
Below is a sample configuration for the ``settings_local.py`` file. It should be placed 
in the root API source code folder.

    DEBUG = True

    # mailgun
    EMAIL_HOST_USER = 'my_user' # only save in local settings
    EMAIL_HOST_PASSWORD = 'my_pass' # only save in local settings

    # RACKSPACE
    RACKSPACE_USERNAME = 'my_user'
    RACKSPACE_APIKEY = 'my_api_key'
    RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = 'mydev_images_'
