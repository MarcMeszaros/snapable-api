# INTRODUCTION #
This is the main API code used for Snapable. It also contains the code that runs
the background workers and includes the API documentation.

# REQUIREMENTS #
Most of the requirements are loaded and built into the docker container by the
build scripts. There are a few system build tools that need to be installed on
your development machine to build the docker container and generate the docs.

The required tools that need to be installed on your development machine.

* [Docker](https://www.docker.com/)
* [Fig](http://www.fig.sh/)
* python/pip (docs)
* node.js (docs)

## Application Requirements ##
Linux system libraries are required for some python libraries to work. This is based 
on the list of python libraries inside the "requirements.txt" file. If libraries 
are changed or added, make sure to update the ``Dockerfile`` to make sure the 
system libraries are part of the build process and update this section.

* python-dev (generic)
* libffi-dev (bcrypt)
* libtiff4-dev  (pillow)
* libjpeg8-dev (pillow)
* zlib1g-dev (pillow)
* libfreetype6-dev (pillow)
* liblcms1-dev (pillow)
* libwebp-dev (pillow)

# DEVELOPMENT #
Development is mostly done in python and using docker. There is currently one suggestion
that should be followed when setting up the project for the first time to make it
easier to build releases. The recommended setup is below.

## Setup ##
Run the following commands:

    > sudo pip install --upgrade
    > sudo pip install virtualenv
    > virtualenv ~/snap_api/
    > cd ~/snap_api/
    > source bin/activate
    > git clone git@bitbucket.org:snapable/api.git
    > cd api
    > pip install -r requirements.txt

## Docker ##
Docker is used for both development and production. The only difference between
development and production are runtime configuration variables and cloud infrastructure.

1. Install [Fig](http://www.fig.sh/)
2. Run ``fig build``
3. Run ``fig up``
4. Run ``fig run api /src/bin/python ./manage.py migrate``
5. Run ``fig run api /src/bin/python ./manage.py loaddata /src/app/data/fixtures/packages.json``

## Unit Tests ##
To run the unit tests, you first need to build the code into a docker:

    > fig build
    > fig run api /src/bin/python ./manage.py test

# RELEASE #
Releasing and deploying the code is relatively simple. To save on space for the docker
container, the API documentation is generated on the development machine and simply
packaged into the final container. Because of this, please make sure to read the
development section above to make it easier to build a release docker container.

    > cd ~/snap_api/
    > source bin/activate
    > cd api
    > pip install -r requirements.txt
    > ./build.sh

# CONFIGURATION #
Configuration is done at runtime using environment variables. Below is a list of
environment variables that can be set for production use instead of the development
defaults. 

| Name                          | Description                                      
|-------------------------------|---------------------------------------------------------------------
| HOST_IP                       | An extra host to allow request to come from for django (default: '')
| DEBUG                         | If debug traces should be displayed [true/false] (default: false)
| DATABASE_NAME                 | The database table name (default: snapabledb)
| DATABASE_USER                 | The database user (default: snapableusr)
| DATABASE_PASSWORD             | The database password
| DATABASE_HOST                 | The database host to use (default: 127.0.0.1)
| DATABASE_PORT                 | The database port to use (default: 3306)
| EMAIL_HOST                    | The SMTP host (default: smtp.mailgun.org)
| EMAIL_PORT                    | The SMTP port (default: 587)
| EMAIL_USE_TLS                 | If TLS should be used [true/false] (default: true)
| EMAIL_HOST_USER               | The email host user
| EMAIL_HOST_PASSWORD           | Email host password
| RACKSPACE_USERNAME            | The rackspace username
| RACKSPACE_APIKEY              | The rackspace API key
| CLOUDFILES_IMAGES_PREFIX      | Cloudfiles images storage filename prefix (default: dev_images_)
| CLOUDFILES_DOWNLOAD_PREFIX    | Cloudfiles download prefix (default: dev_downloads_)
| CLOUDFILES_WATERMARK_PREFIX   | Cloudfiles watermark folder (default: dev_watermark)
| CLOUDFILES_PUBLIC_NETWORK     | Should the client use the internet? [true/false] (default: true)
| GUNICORN_HOST                 | The host for Gunicorn to listen on (default: 127.0.0.1)
| GUNICORN_PORT                 | The port for Gunicorn to listen on (default: 8000)
| REDIS_HOST                    | The redis host to use for application data (default: 127.0.0.1)
| REDIS_PORT                    | The redis port to connect to (default: 6379)
| REDIS_DB                      | The default redis database (default: 0)
| STRIPE_KEY_SECRET             | The secret key for the Stripe API
| STRIPE_KEY_PUBLIC             | The public key for the Stripe API
| STRIPE_CURRENCY               | The currency to charge in (default: usd)
| CELERY_BROKER_HOST            | The celery broker host (default: 127.0.0.1)
| CELERY_BROKER_PORT            | The celery broker port (default: 5672)
| CELERY_BROKER_URL             | The complete broker url (default: redis://CELERY_BROKER_HOST:CELERY_BROKER_PORT/0)
| CELERY_RESULT_HOST            | The celery result host (default: 127.0.0.1)
| CELERY_RESULT_PORT            | The celery result port (default: 5672)
| CELERY_RESULT_URL             | The complete result url (default: redis://CELERY_RESULT_HOST:CELERY_RESULT_PORT/0)
| SENTRY_DSN                    | The DSN string to use for Sentry (default: '')
| NEW_RELIC_ENVIRONMENT         | The environment for logging [staging/production] (default: development)