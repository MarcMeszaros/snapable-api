from django.conf.urls import patterns, include, url
import api.v1

api_v1 = api.v1.SnapableApi()

urlpatterns = patterns('',
    # define all the API versions here
    # the latest API version should work without the number as well

    # all '1/' paths resolve to API version 1
    url(r'', include(api_v1.urls)),
)
