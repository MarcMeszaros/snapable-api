# django/libs
from django.contrib import admin

# This global object represents the admin site, for the common case.
site = admin.site
site.index_template = 'admin/index.html'

site.disable_action('delete_selected')