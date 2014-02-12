# python
from datetime import datetime

# django/libs
from django.conf import settings
from django.http import HttpResponse

# snapable
from api.auth import ServerAuthentication
from api.private_v1.resources import UserResource

def index(request):
    return HttpResponse("You're looking at ajax index.")

def total_signups(request, start=0, end=None):
    startdate = datetime.utcfromtimestamp(float(start))
    enddate = datetime.utcnow()
    if end is not None:
        enddate = datetime.utcfromtimestamp(float(end))

    kwargs = {
        'created_at__gte': startdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'created_at__lte': enddate.strftime('%Y-%m-%dT%H:%M:%SZ'),
    }

    # sign the API request
    key, secret = settings.APIKEY.items()[0]
    res = UserResource()
    return res.dispatch_list(ServerAuthentication.sign_request(request, key, secret), **kwargs)