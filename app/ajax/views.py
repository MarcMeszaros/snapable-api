"""AJAX enpoints"""
# python
import json
from datetime import datetime

# django/libs
from django.db.models import Sum
from django.http import HttpResponse

# snapable
from data.models import Event, Order, Photo, User

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

def _event_guest_count_avg(start, end):
    events = Event.objects.filter(end_at__gte=start, end_at__lte=end)
    guest_sum = 0
    for event in events:
        guest_sum += event.guest_count

    # avoid division by 0
    if len(events) > 0:
        return float(guest_sum) / len(events)
    else:
        return 0

def _events_with_photos(start, end):
    events = Event.objects.filter(end_at__gte=start, end_at__lte=end)
    events_with_photos = 0
    for event in events:
        if event.photo_count > 0:
            events_with_photos += 1

    return events_with_photos

### Actual Functions ###
def index(request):
    return HttpResponse("You're looking at ajax index.")

def metrics(request, start=0, end=None):
    startdate = datetime.utcfromtimestamp(float(start))
    enddate = datetime.utcnow()
    if end is not None:
        enddate = datetime.utcfromtimestamp(float(end))

    orders_metrics = Order.objects.filter(created_at__gte=startdate, created_at__lte=enddate).aggregate(Sum('amount'), Sum('amount_refunded'))

    response_data = {
        'metrics': {
            'avg_photos_per_event': _event_photo_count_avg(startdate, enddate),
            'avg_guests_per_event': _event_guest_count_avg(startdate, enddate),
            'orders': orders_metrics,
            'past_events_count': Event.objects.filter(end_at__gte=startdate, end_at__lte=enddate).count(),
            'past_events_with_photos_count': _events_with_photos(startdate, enddate),
            'photo_count': Photo.objects.filter(created_at__gte=startdate, created_at__lte=enddate).count(),
            'total_actives': User.objects.filter(last_login__gte=startdate, last_login__lte=enddate).count(),
            'total_signups': User.objects.filter(created_at__gte=startdate, created_at__lte=enddate).count(),
            'upcoming_events_count': Event.objects.filter(end_at__gte=enddate).count(),
        }
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')
