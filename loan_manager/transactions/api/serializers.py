# Libs imports
from ipware import get_client_ip

# Django imports
from rest_framework import serializers

# Transactions app imports
from transactions.models import Loan, Payment


class LoanSerializer(serializers.ModelSerializer):
    end_date = serializers.DateField()
    interest_type = serializers.IntegerField()
    full_debt = serializers.SerializerMethodField('get_full_debt')
    total_paid = serializers.SerializerMethodField('get_total_paid')
    outstanding_balance = serializers.SerializerMethodField('get_outstanding_balance')

    class Meta:
        model = Loan
        fields = ['id', 
                  'user_account', 
                  'nominal_value', 
                  'interest_type', 
                  'interest_rate', 
                  'ip_address', 
                  'request_date', 
                  'end_date', 
                  'bank', 
                  'client',
                  'full_debt',
                  'total_paid', 
                  'outstanding_balance']
        read_only_fields = ['id', 
                            'user_account', 
                            'ip_address', 
                            'request_date']
        
    def get_full_debt(self, obj):
        return obj.get_full_debt
    
    def get_total_paid(self, obj):
        return obj.get_total_paid
    
    def get_outstanding_balance(self, obj):
        return obj.get_outstanding_balance
                 
    def validate(self, data):
        instance = getattr(self, 'instance', None)
        if instance:
            if data['nominal_value'] < instance.get_total_paid:
                raise serializers.ValidationError(
                    {'detail':"The nominal value can't be less than the total paid."}
                )
        return data
    
    def validate_nominal_value(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {'detail':"The value needs to be greater than zero."}
            )
        return value
    
    def create(self, validated_data):
        if self.is_valid():
            ip_address = get_client_ip(self.context['request'])[0]
            loan = Loan.objects.create(
                user_account=self.context['request'].user,
                nominal_value=validated_data['nominal_value'],
                interest_rate=validated_data['interest_rate'],
                ip_address=ip_address,
                end_date=validated_data['end_date'],
                bank=validated_data['bank'],
                client=validated_data['client'],
                interest_type=validated_data['interest_type']
            )
            return loan
    
    def update(self, instance, validated_data):
        if self.is_valid():
            instance.nominal_value=validated_data['nominal_value']
            instance.interest_rate=validated_data['interest_rate']
            instance.end_date=validated_data['end_date']
            instance.bank=validated_data['bank']
            instance.client=validated_data['client']
            instance.interest_type=validated_data['interest_type']
            instance.save()
            return instance

        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        
    def validate(self, data):
        instance = getattr(self, 'instance', None)
        total_paid = data['loan'].get_total_paid
        full_debt = data['loan'].get_full_debt
        if instance:
            value_difference = data['value'] - instance.value
            total_paid += value_difference
            if total_paid > full_debt:
                raise serializers.ValidationError(
                    {'detail':"The total paid needs to be less or equal than the full debt."}
                )
        else:
            total_paid += data['value']
            if total_paid > full_debt:
                raise serializers.ValidationError(
                    {'detail':"The total paid needs to be less or equal than the full debt."}
                )
        return data
        
    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {'detail':"The value needs to be greater than zero."}
            )
        return value
    
    def validate_loan(self, value):
        if value.user_account != self.context['request'].user:
            raise serializers.ValidationError(
                {'detail':"You need to be the loan's user."}
            )
        return value
        
    def create(self, validated_data):      
        payment = Payment.objects.create(
            loan=validated_data['loan'],
            date=validated_data['date'],
            value=validated_data['value']
        )
        return payment
    
    def update(self, instance, validated_data):
        instance.loan=validated_data['loan']
        instance.date=validated_data['date']
        instance.value=validated_data['value']
        instance.save()
        return instance