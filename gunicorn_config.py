import multiprocessing
import netifaces
import os

# some config variables
cfg_eth0_address = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'] # usually the public IP on Rackspace/VM
cfg_eth1_address = netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr'] # usually the internal IP on Rackspace/VM
cfg_port = '8000' # the port we should bind to

# the gunicorn parameters
bind = cfg_eth1_address + ':' + cfg_port
workers = multiprocessing.cpu_count() * 2 + 1
#daemon = True # disable daemon for now because of a weird worker spawning problem, just add "&" to your command to detach the terminal

# setup logging
accesslog = os.path.join(os.getcwd(), 'logs', 'access.log')
errorlog = os.path.join(os.getcwd(), 'logs', 'error.log')