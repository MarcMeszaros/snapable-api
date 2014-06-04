import multiprocessing

# the gunicorn parameters
cfg_port = '8000' # the port we should bind to
bind = '127.0.0.1:{0}'.format(cfg_port)

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync' # default: sync; alternate: gevent
proc_name = 'snap_api'

# logging
#accesslog = '-'
errorlog = '-'
