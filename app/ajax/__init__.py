from django.conf.urls import patterns, url

import views

urls = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^metrics(/(?P<start>\d+)(/(?P<end>\d+))?)?$', views.metrics, name='metrics'),
)
