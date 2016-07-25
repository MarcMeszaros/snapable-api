# -*- coding: utf-8 -*-
from __future__ import absolute_import

import envitro
import pymysql

pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': envitro.str('DATABASE_NAME'),
        'USER': envitro.str('DATABASE_USER'),
        'PASSWORD': envitro.str('DATABASE_PASSWORD'),
        'HOST': envitro.str('DATABASE_HOST', '127.0.0.1'),
        'PORT': envitro.int('DATABASE_PORT', 3306),
    }
}
