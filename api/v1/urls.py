from django.conf.urls import patterns, include, url
from piston.resource import Resource
from api.v1.handlers import ApiHandler

api_resource = Resource(handler=ApiHandler)

urlpatterns = patterns('',
	# simple matching pattern
	url(r'^(?P<data>[-_a-zA-Z0-9]+)/?', api_resource),
)