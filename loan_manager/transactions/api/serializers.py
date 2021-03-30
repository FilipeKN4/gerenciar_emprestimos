#Django imports
from rest_framework import serializers

# Transactions app imports
from transactions.models import Loan, Payment


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        
    def create(self, validated_data):
        if self.loan_validations(validated_data['nominal_value']):
            loan = Loan.objects.create(
                user_account=self.context['request'].user,
                nominal_value=validated_data['nominal_value'],
                interest_rate=validated_data['interest_rate'],
                bank=validated_data['bank'],
                client=validated_data['client']
            )
            return loan
    
    def update(self, instance, validated_data):
        if self.loan_validations(validated_data['nominal_value']):
            instance.nominal_value=validated_data['nominal_value']
            instance.interest_rate=validated_data['interest_rate']
            instance.bank=validated_data['bank']
            instance.client=validated_data['client']
            instance.save()
            return instance
    
    def loan_validations(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "The value needs to be greater than zero."
            )
        return True

        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        
    def create(self, validated_data):
        if self.payment_validations(validated_data['loan'], 
                                    validated_data['value']):        
            payment = Payment.objects.create(
                loan=validated_data['loan'],
                date=validated_data['date'],
                value=validated_data['value']
            )
            return payment
    
    def update(self, instance, validated_data):
        if self.payment_validations(instance.loan, 
                                    validated_data['value'], 
                                    instance): 
            instance.date=validated_data['date']
            instance.value=validated_data['value']
            instance.save()
            return instance
    
    def payment_validations(self, loan, value, payment=None):
        total_paid = loan.get_total_paid
        if payment:
            value_difference = value - payment.value
            total_paid += value_difference
            if total_paid > loan.get_full_debt:
                raise serializers.ValidationError(
                    "The total paid needs to be less or equal than the full debt."
                )
        else:
            total_paid += value
            if total_paid > loan.get_full_debt:
                raise serializers.ValidationError(
                    "The total paid needs to be less or equal than the full debt."
                )
        if value <= 0:
            raise serializers.ValidationError(
                "The value needs to be greater than zero."
            )
        return True