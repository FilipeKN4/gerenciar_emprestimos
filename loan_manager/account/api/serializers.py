#Django imports
from rest_framework import serializers

# Account app imports
from account.models import Account


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'