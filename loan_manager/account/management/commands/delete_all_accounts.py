# Django imports
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token

# Account app imports
from account.models import Account

class Command(BaseCommand):
    help = 'Delete all accounts'

    def handle(self, *args, **options):
        Account.objects.all().delete()
        Token.objects.all().delete()
