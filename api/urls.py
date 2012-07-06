from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api.views.home', name='home'),
    # url(r'^api/', include('api.foo.urls')),

    # all '1/' paths resolve to API version 1
    url(r'^1/', include('api.v1.urls')),
)
