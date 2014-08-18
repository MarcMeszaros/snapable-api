from django.conf.urls import patterns, include, url

# the hook files
from .stripe import urls as stripe_urls # syntax to prevent namespace collision

urls = patterns('',
    url(r'^stripe/', include(stripe_urls)),
)
