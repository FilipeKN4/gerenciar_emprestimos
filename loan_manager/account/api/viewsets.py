#Django imports
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, permissions

# Account app imports
from account.api import serializers
from account.models import Account


class AccountViewSet(viewsets.ModelViewSet):
    """API endpoint that allows accounts to be viewed or edited."""
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = serializers.AccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]

    @method_decorator(cache_page(60 * 15, key_prefix='account_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15, key_prefix='account_detail'))
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
