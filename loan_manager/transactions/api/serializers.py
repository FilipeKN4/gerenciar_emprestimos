#Django imports
from rest_framework import serializers

# Transactions app imports
from transactions.models import Loan, Payment


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        
    def create(self, validated_data):
        loan = Loan.objects.create(
            user_account=self.context['request'].user,
            nominal_value=validated_data['nominal_value'],
            interest_rate=validated_data['interest_rate'],
            bank=validated_data['bank'],
            client=validated_data['client']
        )
        return loan
    
    def update(self, instance, validated_data):
        instance.nominal_value=validated_data['nominal_value']
        instance.interest_rate=validated_data['interest_rate']
        instance.bank=validated_data['bank']
        instance.client=validated_data['client']
        instance.save()
        return instance

        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        
    def create(self, validated_data):
        payment = Payment.objects.create(
            loan=validated_data['loan'],
            date=validated_data['date'],
            value=validated_data['value']
        )
        return payment
    
    def update(self, instance, validated_data):
        instance.date=validated_data['date'],
        instance.value=validated_data['value']
        instance.save()
        return instance