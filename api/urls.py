from django.conf.urls import patterns, include, url

import api.v1
import api.private_v1

api_v1 = api.v1.SnapableApi()
private_v1 = api.private_v1.SnapableApi()

urlpatterns = patterns('',
    # define all the API versions here
    # the latest API version should work without the number as well

    # public APIs
    url(r'', include(api_v1.urls)),

    # private APIs
    url(r'', include(private_v1.urls)),
)
