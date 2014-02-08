import django.contrib.admin.sites

class AdminSite(django.contrib.admin.sites.AdminSite):
    pass

# This global object represents the admin site, for the common case.
site = AdminSite()