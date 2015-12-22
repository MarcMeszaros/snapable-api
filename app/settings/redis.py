# -*- coding: utf-8 -*-
import envitro
import envitro.docker

##### Redis #####
REDIS_HOST = envitro.str('REDIS_HOST', envitro.docker.host('RD', '127.0.0.1'))
REDIS_PORT = envitro.int('REDIS_PORT', envitro.docker.port('RD', 6379))
REDIS_DB = envitro.int('REDIS_DB', 0)
