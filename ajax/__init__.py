from django.conf.urls import patterns, url

import views

urls = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^total_signups(/(?P<start>\d+)(/(?P<end>\d+))?)?$', views.total_signups, name='total_signups'),
    url(r'^past_events(/(?P<start>\d+)(/(?P<end>\d+))?)?$', views.past_events, name='past_events'),
    url(r'^photos_count(/(?P<start>\d+)(/(?P<end>\d+))?)?$', views.photos_count, name='photos_count'),
    url(r'^upcoming_events(/(?P<start>\d+)(/(?P<end>\d+))?)?$', views.upcoming_events, name='upcoming_events'),
    url(r'^events_with_photo_count/(?P<photo_count>\d+)(/(?P<start>\d+)(/(?P<end>\d+))?)?$', views.events_with_photo_count, name='events_with_photo_count'),
)