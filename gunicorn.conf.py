import multiprocessing
import os
import socket

# get the folder path
PROJECT_PATH = os.path.dirname(__file__)

# create the 'logs' folder(s) if it doesn't already exist
if not os.path.exists(os.path.join(PROJECT_PATH, 'logs')):
    os.makedirs(os.path.join(PROJECT_PATH, 'logs'))

# the gunicorn parameters
cfg_port = '8000' # the port we should bind to
bind = '127.0.0.1:{0}'.format(cfg_port)

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync' # default: sync; alternate: gevent
proc_name = 'snap_api'

# logging
#accesslog = '-'
errorlog = '-'
