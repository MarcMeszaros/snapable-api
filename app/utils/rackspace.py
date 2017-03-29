# django/tastypie/libs
import envitro
import pyrax
import warnings

from django.conf import settings

# pyrax connection
RACKSPACE_USERNAME = envitro.str('RACKSPACE_USERNAME')
RACKSPACE_APIKEY = envitro.str('RACKSPACE_APIKEY')

# attributes
try:
    pyrax.set_setting('identity_type', 'rackspace')
    pyrax.set_setting('region', 'DFW')
    pyrax.set_credentials(RACKSPACE_USERNAME, RACKSPACE_APIKEY)
    cloud_files = pyrax.connect_to_cloudfiles(public=settings.CLOUDFILES_PUBLIC_NETWORK)
except:
    warnings.warn('Not able to setup CloudFiles connection')
    cloud_files = None
