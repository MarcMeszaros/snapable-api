import django.contrib.admin.sites
from django.conf.urls import patterns, url

import ajax.views

class AdminSite(django.contrib.admin.sites.AdminSite):

    def get_urls(self):
        base_patterns = super(AdminSite, self).get_urls()
        new_patters = patterns('',
            (r'^ajax/', ajax.views.index),
        )

        return new_patters + base_patterns

# This global object represents the admin site, for the common case.
site = AdminSite()