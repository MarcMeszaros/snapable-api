# -*- coding: utf-8 -*-
import envitro
import etcd

ETCD_HOST = envitro.str('ETCD_HOST', '172.17.42.1') # coreos default
ETCD_PORT = envitro.int('ETCD_PORT', 2379)
ETCD_KEY_REDIS = envitro.str('ETCD_KEY_REDIS', '/services/redis')

REDIS_HOST = envitro.str('REDIS_HOST', allow_none=True)
REDIS_PORT = envitro.int('REDIS_PORT', allow_none=True)
# if the redis host and port were not explicitly set, try and infer them from etcd
if not (REDIS_HOST and REDIS_PORT):
    try:
        client = etcd.Client(host=ETCD_HOST, port=ETCD_PORT, read_timeout=5)
        vals = client.read(ETCD_KEY_REDIS).children.next().value.rsplit(':', 1)
        REDIS_HOST = vals[0]
        REDIS_PORT = int(vals[1])
    except:
        print('No ETCD connection. Using localhost defaults.')
        REDIS_HOST = '127.0.0.1'
        REDIS_PORT = 6379

##### Redis #####
REDIS_DB = envitro.int('REDIS_DB', 0)
