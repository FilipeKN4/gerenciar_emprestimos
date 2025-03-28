# Django imports
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token

# Account app imports
from account.models import Account

class Command(BaseCommand):
    help = 'Create some user accounts'

    def handle(self, *args, **options):
        # Admin
        Account.objects.create_superuser(
            email='admin_test@teste.com',
            username='admin_test',
            password='123'
        )

        # Commom users
        Account.objects.create_user(
            email='joao_mcenroe@teste.com',
            username='joao_mcenroe',
            password='123'
        )

        Account.objects.create_user(
            email='steffi_graf@teste.com',
            username='steffi_graf',
            password='123'
        )
