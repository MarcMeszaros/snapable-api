from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

import api.v1
import api.private_v1

api_v1 = api.v1.SnapableApi()
private_v1 = api.private_v1.SnapableApi()

urlpatterns = patterns('',
    # redirect the root API to prevent error pages
    url(r'^$', lambda x: HttpResponseRedirect('http://snapable.com/')),

    ## define all the API versions here ##
    # public APIs
    url(r'', include(api_v1.urls)),

    # private APIs
    url(r'', include(private_v1.urls)),
)
