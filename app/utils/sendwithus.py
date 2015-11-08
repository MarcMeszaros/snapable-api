from __future__ import absolute_import

# django/libs
import sendwithus
from django.conf import settings

api = sendwithus.api(api_key=settings.SENDWITHUS_KEY)