# Libs imports
import datetime

# Django imports
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

# Apps imports
from account.models import Account
from transactions.models import Loan, Payment


class TestTransactionsAPIViews(APITestCase):
    
    def setUp(self):
        self.first_account = Account.objects.create(
            username='jon',
            email='jon@mail.com',
            password='password123'
        )
        self.second_account = Account.objects.create(
            username='daenerys',
            email='daenerys@mail.com',
            password='password123'
        )
        self.loan = Loan.objects.create(
            user_account=self.first_account,
            nominal_value=20000,
            interest_rate=5.5,
            bank='BRB',
            client='Jon',
            interest_type=1
        )
        self.payment = Payment.objects.create(
            loan = self.loan,
            value = 2500,
            date = datetime.datetime.now()
        )
        self.login()
        
    def login(self):
        self.client.force_authenticate(self.first_account)
    
    # Tests for GET requests 
    def test_transactions_overview(self): 
        response = self.client.get(reverse('transactions_overview'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_loans_list(self): 
        response = self.client.get(reverse('loans_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_loan_detail_get(self): 
        response = self.client.get(reverse('loan_detail', args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_loan_detail_other_user(self):
        self.client.logout()
        self.client.force_authenticate(self.second_account)
        response = self.client.get(reverse('loan_detail', args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
                         {"detail": "You don't have permission to view this content."})
    
    def test_payments_per_loan(self): 
        response = self.client.get(reverse('payments_per_loan', args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_payments_per_loan_other_user(self):
        self.client.logout()
        self.client.force_authenticate(self.second_account)
        response = self.client.get(reverse('payments_per_loan', args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
                         {"detail": "You don't have permission to view this content."})
        
    def test_loan_outstanding_balance(self): 
        response = self.client.get(reverse('loan_outstanding_balance', args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_loan_outstanding_other_user(self):
        self.client.logout()
        self.client.force_authenticate(self.second_account)
        response = self.client.get(reverse('loan_outstanding_balance', args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
                         {"detail": "You don't have permission to view this content."})
    
    def test_payments_list(self): 
        response = self.client.get(reverse('payments_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_payment_detail_get(self): 
        response = self.client.get(reverse('payment_detail', args=[self.payment.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_payment_detail_other_user(self):
        self.client.logout()
        self.client.force_authenticate(self.second_account)
        response = self.client.get(reverse('payment_detail', args=[self.payment.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
                         {"detail": "You don't have permission to view this content."})
    
    # Tests for POST requests
    def test_loan_with_simple_interest_post(self):
        data = {
            'user_account': self.first_account.pk, 
            'nominal_value': 20000,
            'interest_rate': 5.5,
            'end_date': '',
            'bank': 'BRB',
            'client': 'Jon',
            'interest_type': 1
        }
        response = self.client.post(reverse('loans_list'), data)
        last_loan = Loan.objects.last()
        request_date  = last_loan.request_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_loan.pk,  
                                         'nominal_value':'20000.00', 
                                         'interest_rate':'5.50', 
                                         'ip_address': last_loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': None,
                                         'bank':'BRB', 
                                         'client':'Jon', 
                                         'interest_type':1, 
                                         'user_account': self.first_account.pk})
    
    def test_loan_with_compound_interest_post(self):
        data = {
            'user_account': self.second_account.pk, 
            'nominal_value': 15000,
            'interest_rate': 6.5,
            'end_date': '2021-05-20T14:50:57.548143Z',
            'bank': 'BRB',
            'client': 'Jon',
            'interest_type': 2
        }
        response = self.client.post(reverse('loans_list'), data)
        last_loan = Loan.objects.last()
        request_date  = last_loan.request_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_loan.pk,  
                                         'nominal_value':'15000.00', 
                                         'interest_rate':'6.50', 
                                         'ip_address': last_loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': '2021-05-20T14:50:57.548143Z',
                                         'bank':'BRB', 
                                         'client':'Jon', 
                                         'interest_type':2, 
                                         'user_account': last_loan.user_account.pk})
    
    def test_payment_post(self):
        data = {
            'loan': self.loan.pk, 
            'date': '2021-05-20T14:50:57.548143Z',
            'value': 5000,
        }
        response = self.client.post(reverse('payments_list'), data)
        last_payment = Payment.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_payment.pk,  
                                         'value':'5000.00', 
                                         'date': '2021-05-20T14:50:57.548143Z', 
                                         'loan': self.loan.pk})
    
    # Tests for PUT requests
    def test_loan_put(self):
        data = {
            'user_account': self.first_account.pk,
            'nominal_value': 25000,
            'interest_rate': 7.5,
            'end_date': '',
            'bank': 'BRB',
            'client': 'Jon Snow',
            'interest_type': 1
        }
        response = self.client.put(reverse('loan_detail', 
                                           args=[self.loan.pk]), 
                                   data)
        loan = Loan.objects.get(pk=self.loan.pk)
        request_date  = loan.request_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': loan.pk,  
                                         'nominal_value':'25000.00', 
                                         'interest_rate':'7.50', 
                                         'ip_address': loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': None,
                                         'bank':'BRB', 
                                         'client':'Jon Snow', 
                                         'interest_type':1, 
                                         'user_account': self.first_account.pk})
    
    def test_payment_put(self):
        data = {
            'loan': self.loan.pk, 
            'date': '2021-06-20T14:50:57.548143Z',
            'value': 7000,
        }
        response = self.client.put(reverse('payment_detail', 
                                           args=[self.payment.pk]), 
                                   data)
        payment = Payment.objects.get(pk=self.payment.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': payment.pk,  
                                         'value':'7000.00', 
                                         'date': '2021-06-20T14:50:57.548143Z', 
                                         'loan': self.loan.pk})
    
    # Tests for DELETE requests
    def test_loan_delete(self):
        loans_length = len(Loan.objects.all())
        response = self.client.delete(reverse('loan_detail', 
                                           args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Loan.objects.all()), loans_length-1)
    
    def test_payment_delete(self):
        payments_length = len(Payment.objects.all())
        response = self.client.delete(reverse('payment_detail', 
                                           args=[self.payment.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Payment.objects.all()), payments_length-1)
        
        