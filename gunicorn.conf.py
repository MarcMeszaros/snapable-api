import multiprocessing
import netifaces
import socket

# some config variables
cfg_eth0_address = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'] # usually the public IP on Rackspace/VM
cfg_eth1_address = netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr'] # usually the internal IP on Rackspace/VM
cfg_port = '8000' # the port we should bind to

# the gunicorn parameters
bind = [
    '127.0.0.1:{0}'.format(cfg_port),
    #'{0}:{1}'.format(cfg_eth0_address, cfg_port), 
    '{0}:{1}'.format(cfg_eth1_address, cfg_port),
]
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync' # default: sync; alternate: gevent
proc_name = 'snap_api'