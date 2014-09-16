# django/libs
from django.contrib.admin.sites import AdminSite

# This global object represents the admin site, for the common case.
site = AdminSite()
site.disable_action('delete_selected')