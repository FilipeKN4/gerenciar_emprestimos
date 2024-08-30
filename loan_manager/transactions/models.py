# Libs imports
import datetime

# Django imports
from django.db import models
from django.db.models import Sum


class Loan(models.Model):
    class InterestType(models.IntegerChoices):
        SIMPLE = 1
        COMPOUND = 2

    user_account = models.ForeignKey('account.Account',
                                on_delete=models.CASCADE)
    nominal_value = models.DecimalField(max_digits=14,
                                        decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5,
                                        decimal_places=2)
    ip_address = models.GenericIPAddressField(null=True)
    request_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=datetime.date.today)
    bank = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    interest_type = models.IntegerField(choices=InterestType.choices,
                                        default=InterestType.SIMPLE)

    def __str__(self):
        return 'Loan from {} to {} on value of {}'.format(self.bank,
                                                     self.client,
                                                     self.nominal_value)

    @property
    def get_months_difference(self):
        request_date = self.request_date
        end_date = self.end_date
        months_difference = ((end_date.year - request_date.year)
                             * 12
                             + (end_date.month - request_date.month))
        return months_difference

    @property
    def get_interest_value(self):
        interest_rate = self.interest_rate/100
        if self.interest_type == self.InterestType.SIMPLE:
            interest_value = self.nominal_value * interest_rate
        else:
            months_difference = self.get_months_difference
            interest_value = (self.nominal_value
                              * (1 + interest_rate)**months_difference)
            interest_value -= self.nominal_value
        return round(interest_value, 2)

    @property
    def get_full_debt(self):
        return self.nominal_value + self.get_interest_value

    @property
    def get_total_paid(self):
        payments = Payment.objects.filter(loan=self).aggregate(Sum('value'))
        return payments['value__sum'] if payments['value__sum'] else 0

    @property
    def get_outstanding_balance(self):
        outstanding_balance = self.get_full_debt - self.get_total_paid
        return round(outstanding_balance, 2)


class Payment(models.Model):
    loan = models.ForeignKey(Loan,
                             on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=14,
                                decimal_places=2)

    def __str__(self):
        return 'Payment from {} to {} on value of {}'.format(self.loan.client,
                                                             self.loan.bank,
                                                             self.value)
