from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            column=1,
            exclude=('django.contrib.*',),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Links'),
            column=2,
            children=[
                {
                    'title': _('Status'),
                    'url': 'http://status.snapable.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://django-grappelli.readthedocs.org/en/latest/',
                    'external': True,
                },
            ]
        ))
