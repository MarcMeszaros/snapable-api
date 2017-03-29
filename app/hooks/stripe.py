# python
import importlib
import json

# django/libs
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# snapable
import utils
from data.models import *

IGNORE_EVENTS = [
    'balance.available',
    'customer.card.created',
    'customer.created',
    'transfer.created',
    'transfer.paid',
]


def charge__refunded(data):
    charge_id = data.object.id
    order = Order.objects.get(charge_id=charge_id)

    # calculate the refunds
    refunded = 0
    for refund in data.object.refunds.data:
        refunded += refund.amount
    order.amount_refunded = refunded

    # if it is completely refunded, just set it
    if data.object.refunded:
        order.amount_refunded = order.amount

    order.save()
    return True

###### Magic Wrapper stuff ######

# Webhooks are always sent as HTTP POST requests, so we want to ensure
# that only POST requests will reach your webhook view. We can do that by
# decorating `webhook()` with `require_POST`.
#
# Then to ensure that the webhook view can receive webhooks, we need
# also need to decorate `webhook()` with `csrf_exempt`.
@require_POST
@csrf_exempt
def index(request):
    success = False
    stripe_event = utils.Dotable(json.loads(request.body))

    # skip the event if it is in the ignore list
    if stripe_event.type in IGNORE_EVENTS:
        return HttpResponse(status=200)

    # Process webhook data in `request.body`
    type_parts = stripe_event.type.split('.') # charge.succeed -> ['charge', 'succeed']
    function_name = '__'.join(type_parts)
    try:
        # get the func, will raise AttributeError if class cannot be found
        func = getattr(importlib.import_module(__name__), function_name)
        success = func(stripe_event.data)
        if success:
            return HttpResponse(status=200)
        else:
            utils.Log.e('Stripe failed to process hook: {0}'.format(stripe_event.request))
            return HttpResponse(status=500)
    except AttributeError as e:
        return HttpResponse(status=200)
    except Exception as e:
        utils.Log.e('Stripe hook exception: [{0}] {1}'.format(type(e).__name__, e))
        return HttpResponse(status=500)

# declare the endpoint (needs to be after the functions)
urls = patterns('',
    url(r'^$', index, name='index'),
)
