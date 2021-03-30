# Libs imports
import socket

# Django imports
from django.db import models


def current_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

class Loan(models.Model):
    user_account = models.ForeignKey('account.Account', 
                                on_delete=models.CASCADE)
    nominal_value = models.DecimalField(max_digits=14, 
                                        decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, 
                                        decimal_places=2)
    ip_address = models.CharField(max_length=30, 
                                  default=current_ip_address)
    request_date = models.DateTimeField(auto_now_add=True)
    bank = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    
    def __str__(self):
        return 'Loan from {} to {} on value of {}'.format(self.bank, 
                                                     self.client, 
                                                     self.nominal_value)
    
    @property
    def get_interest_value(self):
        interest_value = self.nominal_value * (self.interest_rate/100)
        return interest_value
    
    @property
    def get_full_debt(self):
        full_debt = self.nominal_value + self.get_interest_value
        return full_debt
    
    @property
    def get_outstanding_balance(self):
        payments = Payment.objects.filter(loan=self)
        
        outstanding_balance = self.get_full_debt
        for payment in payments:
            outstanding_balance -= payment.value
        return outstanding_balance
    
    @property
    def get_total_paid(self):
        payments = Payment.objects.filter(loan=self)
        total_paid = 0
        for payment in payments:
            total_paid += payment.value
        return total_paid


class Payment(models.Model):
    loan = models.ForeignKey(Loan, 
                             on_delete=models.CASCADE)
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=14, 
                                decimal_places=2)
    
    def __str__(self):
        return 'Payment from {} to {} on value of {}'.format(self.client, 
                                                             self.bank, 
                                                             self.value)
