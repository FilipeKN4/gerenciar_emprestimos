#Django imports
from rest_framework import serializers

# Account app imports
from account.models import Account


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_account = Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user_account
    
    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.set_password(validated_data['password'])
        instance.save()
        return instance