#Django imports
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