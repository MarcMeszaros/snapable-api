from django.conf.urls import patterns, url

import views

urls = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^total_signups(/(?P<start>\d+)(/(?P<end>\d+))?)?$', views.total_signups, name='total_signups'),
)