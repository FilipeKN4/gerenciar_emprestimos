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


class Payment(models.Model):
    loan = models.ForeignKey(Loan, 
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=14, 
                                decimal_places=2)
    
    def __str__(self):
        return 'Payment from {} to {} on value of {}'.format(self.client, 
                                                             self.bank, 
                                                             self.value)
