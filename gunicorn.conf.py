import multiprocessing
import os

# the gunicorn parameters
cfg_port = os.environ.get('GUNICORN_PORT', '8000')
cfg_host = os.environ.get('GUNICORN_HOST', '127.0.0.1')
bind = '{0}:{1}'.format(cfg_host, cfg_port)

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync' # default: sync; alternate: gevent
proc_name = 'snap_api'

# logging
accesslog = '-'
errorlog = '-'
