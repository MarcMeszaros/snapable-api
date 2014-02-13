# django/libs
import django.contrib.admin.sites
from django.conf.urls import patterns, url

class AdminSite(django.contrib.admin.sites.AdminSite):
    pass

# This global object represents the admin site, for the common case.
site = AdminSite()
site.disable_action('delete_selected')