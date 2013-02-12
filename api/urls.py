from django.conf.urls import patterns, include, url
from django.http import HttpResponse, HttpResponseRedirect

import api.private_v1

private_v1 = api.private_v1.SnapableApi()

urlpatterns = patterns('',
    # redirect the root API to prevent error pages
    url(r'^$', lambda x: HttpResponseRedirect('http://snapable.com/')),
    # tell bots not to try and crawl the API
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /*", mimetype="text/plain")),

    ## define all the API versions here ##
    # public APIs
    #url(r'', include(api_v1.urls)),

    # partner APIs
    #url(r'', include(partner_v1.urls)),

    # private APIs
    url(r'', include(private_v1.urls)),
)
