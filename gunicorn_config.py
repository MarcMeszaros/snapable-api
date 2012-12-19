import multiprocessing
import netifaces
import os
import socket

# some config variables
cfg_eth0_address = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'] # usually the public IP on Rackspace/VM
cfg_eth1_address = netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr'] # usually the internal IP on Rackspace/VM
cfg_port = '8000' # the port we should bind to

# if we are not on production use the localhost
if not 'ares' in socket.gethostname():
    cfg_eth1_address = '127.0.0.1'

# the gunicorn parameters
bind = cfg_eth1_address + ':' + cfg_port
workers = multiprocessing.cpu_count() * 2 + 1
daemon = True
worker_class = 'sync' # default: sync; alternate: gevent
pidfile = 'gunicorn.pid'
timeout = 120
graceful_timeout = 120

# setup logging
accesslog = os.path.join(os.getcwd(), 'logs', 'access.log')
errorlog = os.path.join(os.getcwd(), 'logs', 'error.log')