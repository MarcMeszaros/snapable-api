# python
import json
from datetime import datetime

# django/libs
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse

# snapable
from api.auth import ServerAuthentication
from api.private_v1.resources import EventResource, PhotoResource, UserResource
from data.models import Event, Order, Photo

### Helper Functions ###
def _event_photo_count_avg(start, end):
    events = Event.objects.filter(end_at__gte=start, end_at__lte=end)
    photo_sum = 0
    for event in events:
        photo_sum += event.photo_count

    # avoid division by 0
    if len(events) > 0:
        return float(photo_sum) / len(events)
    else:
        return 0

### Actual Functions ###
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

def past_events(request, start=0, end=None):
    startdate = datetime.utcfromtimestamp(float(start))
    enddate = datetime.utcnow()
    if end is not None:
        enddate = datetime.utcfromtimestamp(float(end))

    kwargs = {
        'end_at__gte': startdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'end_at__lte': enddate.strftime('%Y-%m-%dT%H:%M:%SZ'),
    }

    # sign the API request
    key, secret = settings.APIKEY.items()[0]
    res = EventResource()
    return res.dispatch_list(ServerAuthentication.sign_request(request, key, secret), **kwargs)

def photos_count(request, start=0, end=None):
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
    res = PhotoResource()
    return res.dispatch_list(ServerAuthentication.sign_request(request, key, secret), **kwargs)

def upcoming_events(request, start=0, end=None):
    startdate = datetime.utcfromtimestamp(float(start))
    enddate = datetime.utcnow()
    if end is not None:
        enddate = datetime.utcfromtimestamp(float(end))

    kwargs = {
        'end_at__gte': startdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'order_by': 'start',
    }

    # sign the API request
    key, secret = settings.APIKEY.items()[0]
    res = EventResource()
    return res.dispatch_list(ServerAuthentication.sign_request(request, key, secret), **kwargs)

def events_with_photo_count(request, photo_count, start=0, end=None):
    startdate = datetime.utcfromtimestamp(float(start))
    enddate = datetime.utcnow()
    if end is not None:
        enddate = datetime.utcfromtimestamp(float(end))

    kwargs = {
        'photo_count__gte': photo_count,
        'end_at__gte': startdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'end_at__lte': enddate.strftime('%Y-%m-%dT%H:%M:%SZ'),
    }

    # sign the API request
    key, secret = settings.APIKEY.items()[0]
    res = EventResource()
    return res.dispatch_list(ServerAuthentication.sign_request(request, key, secret), **kwargs)

def metrics(request, start=0, end=None):
    startdate = datetime.utcfromtimestamp(float(start))
    enddate = datetime.utcnow()
    if end is not None:
        enddate = datetime.utcfromtimestamp(float(end))

    orders_metrics = Order.objects.filter(created_at__gte=startdate, created_at__lte=enddate).aggregate(Sum('amount'), Sum('amount_refunded'))

    response_data = {
        'metrics': {
            'avg': _event_photo_count_avg(startdate, enddate),
            'orders': orders_metrics,
        }
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')