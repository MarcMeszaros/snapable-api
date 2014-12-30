FROM        ubuntu:trusty
MAINTAINER  Marc Meszaros <marc@snapable.com>

# install dependencies
RUN apt-get update && apt-get -y install \
    git \
    make \
    ntp \
    python \
    python-apt \
    python-dev \
    python-pip \
    python3 \
    python3-dev \
    libffi-dev \
    libfreetype6-dev \
    libjpeg8-dev \
    liblcms1-dev \
    libmysqlclient-dev \
    libtiff4-dev \ 
    libwebp-dev \
    zlib1g-dev \
    && pip install virtualenv

# virtualenv
RUN virtualenv /src

# pip requirement
COPY requirements.txt /tmp/requirements.txt
RUN cd /tmp && /src/bin/pip install -r /tmp/requirements.txt

# app code
COPY *.py /src/app/
COPY *.ini /src/app/
COPY ajax /src/app/ajax/
COPY api /src/app/api/
COPY dashboard /src/app/dashboard/
COPY data /src/app/data/
COPY docs /src/app/docs/
COPY hooks /src/app/hooks/
COPY utils /src/app/utils/
COPY worker /src/app/worker/

# running
EXPOSE 8000
WORKDIR /src/app
CMD ["/src/bin/gunicorn", "wsgi:application", "--pid", "gunicorn.pid"]
#CMD ["/src/bin/newrelic-admin", "run-program", "/src/bin/gunicorn", "wsgi:application", "--pid gunicorn.pid"]
#CMD ["/src/bin/python", "manage.py", "runserver"]