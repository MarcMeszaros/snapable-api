# -*- coding: utf-8 -*-
from __future__ import absolute_import

import envitro
import pymysql

pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': envitro.str('DATABASE_NAME', 'snapabledb'),
        'USER': envitro.str('DATABASE_USER', 'snapableusr'),
        'PASSWORD': envitro.str('DATABASE_PASSWORD', 'snapable12345'),
        'HOST': envitro.str('DATABASE_HOST', '127.0.0.1'),
        'PORT': envitro.int('DATABASE_PORT', 3306),
    }
}
