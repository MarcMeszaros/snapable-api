FROM        ubuntu:trusty
MAINTAINER  Marc Meszaros <marc@snapable.com>

# install dependencies
RUN apt-get update && apt-get -y install \
    ntp \
    git \
    make \
    python \
    python-dev \
    python-apt \
    python-pip \
    python3 \
    python3-dev \
    libmysqlclient-dev \
    libffi-dev \
    libtiff4-dev \ 
    libjpeg8-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms1-dev \
    libwebp-dev \
    && pip install virtualenv

# virtualenv
RUN virtualenv /src

# pip requirement
ADD requirements.txt /tmp/requirements.txt
RUN cd /tmp && /src/bin/pip install -r /tmp/requirements.txt

# app code
ADD *.py /src/app/
ADD *.ini /src/app/
ADD ajax /src/app/ajax/
ADD api /src/app/api/
ADD dashboard /src/app/dashboard/
ADD data /src/app/data/
ADD docs /src/app/docs/
ADD hooks /src/app/hooks/
ADD utils /src/app/utils/
ADD worker /src/app/worker/

# running
EXPOSE 8000
WORKDIR /src/app
CMD ["/src/bin/gunicorn", "wsgi:application", "--pid", "gunicorn.pid"]
#{{ root }}/bin/newrelic-admin run-program {{ root }}/bin/gunicorn wsgi:application --pid {{ root }}/api/gunicorn.pid
#CMD ["/src/bin/python", "manage.py", "runserver"]