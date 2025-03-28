#Django imports
from rest_framework import serializers

# Account app imports
from account.models import Account


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    is_admin = serializers.BooleanField()
    is_active = serializers.BooleanField()

    class Meta:
        model = Account
        fields = ['id',
                  'email',
                  'username',
                  'password',
                  'first_name',
                  'last_name',
                  'is_admin',
                  'is_active',
                  'is_staff',
                  'is_superuser']
        read_only_fields = ['id',
                            'is_staff',
                            'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data['is_admin']:
            user_account = Account.objects.create_superuser(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password']
            )
        else:
            user_account = Account.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password']
            )
        user_account.first_name = validated_data['first_name']
        user_account.last_name = validated_data['last_name']
        return user_account

    def update(self, instance, validated_data):
        if validated_data['is_admin']:
            instance.is_admin = validated_data['is_admin']
            instance.is_staff = True
            instance.is_superuser = True
        elif not validated_data['is_admin']:
            instance.is_admin = validated_data['is_admin']
            instance.is_staff = False
            instance.is_superuser = False
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.set_password(validated_data['password'])
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance
