from django.core.management.base import BaseCommand, CommandError

from api.models import ApiAccount, ApiKey
from data.models import Account, Event

class Command(BaseCommand):

    def handle(self, *args, **options):
        from django.conf import settings
        if settings.DEBUG:
            # the API test
            api_account, _ = ApiAccount.objects.get_or_create(email='it@snapable.com', company='Snapable')
            api_key, _ = ApiKey.objects.get_or_create(account=api_account, key='key123', secret='sec123', version=ApiKey.API_PRIVATE_V1)
