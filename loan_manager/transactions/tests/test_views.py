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
        self.second_loan = Loan.objects.create(
            user_account=self.second_account,
            nominal_value=20000,
            interest_rate=5.5,
            bank='BRB',
            client='Daenerys',
            interest_type=1
        )
        self.payment = Payment.objects.create(
            loan = self.loan,
            value = 2500,
            date = datetime.date.today()
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
        loans_length = Loan.objects.all().count()
        data = { 
            'nominal_value': 20000,
            'interest_rate': 5.5,
            'end_date': '2021-10-10',
            'bank': 'BRB',
            'client': 'Jon',
            'interest_type': 1
        }
        response = self.client.post(reverse('loans_list'), data)
        last_loan = Loan.objects.last()
        request_date  = last_loan.request_date.strftime("%Y-%m-%d") 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_loan.pk,  
                                         'user_account': last_loan.user_account.pk,
                                         'nominal_value':'20000.00',
                                         'interest_type':1,
                                         'interest_rate':'5.50', 
                                         'ip_address': last_loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': '2021-10-10',
                                         'bank':'BRB', 
                                         'client':'Jon',  
                                         'full_debt': last_loan.get_full_debt, 
                                         'total_paid': last_loan.get_total_paid, 
                                         'outstanding_balance': last_loan.get_outstanding_balance})
        self.assertEqual(Loan.objects.all().count(), loans_length+1)
    
    def test_loan_post_for_other_users(self):
        loans_length = Loan.objects.all().count()
        data = {
            'user_account': self.second_account.pk, 
            'nominal_value': 20000,
            'interest_rate': 5.5,
            'end_date': '2021-10-10',
            'bank': 'BRB',
            'client': 'Jon',
            'interest_type': 1
        }
        response = self.client.post(reverse('loans_list'), data)
        last_loan = Loan.objects.last()
        request_date  = last_loan.request_date.strftime("%Y-%m-%d") 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_loan.pk,  
                                         'user_account': last_loan.user_account.pk,
                                         'nominal_value':'20000.00',
                                         'interest_type':1,
                                         'interest_rate':'5.50', 
                                         'ip_address': last_loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': '2021-10-10',
                                         'bank':'BRB', 
                                         'client':'Jon',  
                                         'full_debt': last_loan.get_full_debt, 
                                         'total_paid': last_loan.get_total_paid, 
                                         'outstanding_balance': last_loan.get_outstanding_balance})
        self.assertEqual(Loan.objects.all().count(), loans_length+1)
        self.assertEqual(last_loan.user_account, self.first_account)
    
    def test_loan_post_with_negative_nominal_value(self):
        loans_length = Loan.objects.all().count()
        data = {
            'user_account': self.first_account.pk, 
            'nominal_value': -20000,
            'interest_rate': 5.5,
            'end_date': '2021-10-10',
            'bank': 'BRB',
            'client': 'Jon',
            'interest_type': 1
        }
        response = self.client.post(reverse('loans_list'), data)
        last_loan = Loan.objects.last()
        request_date  = last_loan.request_date.strftime("%Y-%m-%d") 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "The value needs to be greater than zero.")
    
    def test_loan_with_compound_interest_post(self):
        loans_length = Loan.objects.all().count()
        data = { 
            'nominal_value': 15000,
            'interest_rate': 6.5,
            'end_date': '2021-05-20',
            'bank': 'BRB',
            'client': 'Jon',
            'interest_type': 2
        }
        response = self.client.post(reverse('loans_list'), data)
        last_loan = Loan.objects.last()
        request_date  = last_loan.request_date.strftime("%Y-%m-%d") 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_loan.pk,
                                         'user_account': last_loan.user_account.pk,
                                         'nominal_value':'15000.00', 
                                         'interest_type':2,
                                         'interest_rate':'6.50', 
                                         'ip_address': last_loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': '2021-05-20',
                                         'bank':'BRB', 
                                         'client':'Jon',  
                                         'full_debt': last_loan.get_full_debt, 
                                         'total_paid': last_loan.get_total_paid, 
                                         'outstanding_balance': last_loan.get_outstanding_balance})
        self.assertEqual(Loan.objects.all().count(), loans_length+1)
    
    def test_payment_post(self):
        payments_length = Payment.objects.all().count()
        data = {
            'loan': self.loan.pk, 
            'date': '2021-05-20',
            'value': 5000,
        }
        response = self.client.post(reverse('payments_list'), data)
        last_payment = Payment.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_payment.pk,  
                                         'value':'5000.00', 
                                         'date': '2021-05-20', 
                                         'loan': last_payment.loan.pk})
        self.assertEqual(Payment.objects.all().count(), payments_length+1)
        
    def test_payment_post_for_other_users_loan(self):
        payments_length = Payment.objects.all().count()
        data = {
            'loan': self.second_loan.pk, 
            'date': '2021-05-20',
            'value': 5000,
        }
        response = self.client.post(reverse('payments_list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "You need to be the loan's user.")
    
    def test_payment_post_bigger_than_loan(self):
        payments_length = Payment.objects.all().count()
        data = {
            'loan': self.loan.pk, 
            'date': '2021-05-20',
            'value': 30000,
        }
        response = self.client.post(reverse('payments_list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                            "The total paid needs to be less or equal than the full debt.")
    
    def test_payment_post_with_negative_value(self):
        payments_length = Payment.objects.all().count()
        data = {
            'loan': self.second_loan.pk, 
            'date': '2021-05-20',
            'value': -5000,
        }
        response = self.client.post(reverse('payments_list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "The value needs to be greater than zero.")
    
    # Tests for PUT requests
    def test_loan_put(self):
        data = {
            'user_account': self.first_account.pk,
            'nominal_value': 25000,
            'interest_rate': 7.5,
            'end_date': '2021-10-10',
            'bank': 'BRB',
            'client': 'Jon Snow',
            'interest_type': 1
        }
        response = self.client.put(reverse('loan_detail', 
                                           args=[self.loan.pk]), 
                                   data)
        loan = Loan.objects.get(pk=self.loan.pk)
        request_date  = loan.request_date.strftime("%Y-%m-%d") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': loan.pk,
                                         'user_account': self.first_account.pk,
                                         'nominal_value':'25000.00',
                                         'interest_type':1,
                                         'interest_rate':'7.50', 
                                         'ip_address': loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': '2021-10-10',
                                         'bank':'BRB', 
                                         'client':'Jon Snow', 
                                         'full_debt': loan.get_full_debt, 
                                         'total_paid': loan.get_total_paid, 
                                         'outstanding_balance': loan.get_outstanding_balance})
        
    def test_loan_put_with_nominal_value_less_than_total_paid(self):
        data = {
            'nominal_value': 2000,
            'interest_rate': 7.5,
            'end_date': '2021-10-10',
            'bank': 'BRB',
            'client': 'Jon Snow',
            'interest_type': 1
        }
        response = self.client.put(reverse('loan_detail', 
                                           args=[self.loan.pk]), 
                                   data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "The nominal value can't be less than the total paid.")
    
    def test_loan_put_with_negative_nominal_value(self):
        data = {
            'nominal_value': -2000,
            'interest_rate': 7.5,
            'end_date': '2021-10-10',
            'bank': 'BRB',
            'client': 'Jon Snow',
            'interest_type': 1
        }
        response = self.client.put(reverse('loan_detail', 
                                           args=[self.loan.pk]), 
                                   data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "The value needs to be greater than zero.")
    
    def test_loan_put_for_other_users(self):
        data = {
            'user_account': self.second_account.pk,
            'nominal_value': 20000,
            'interest_rate': 7.5,
            'end_date': '2021-10-10',
            'bank': 'BRB',
            'client': 'Jon Snow',
            'interest_type': 1
        }
        response = self.client.put(reverse('loan_detail', 
                                           args=[self.loan.pk]), 
                                   data)
        loan = Loan.objects.get(pk=self.loan.pk)
        request_date  = loan.request_date.strftime("%Y-%m-%d")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': loan.pk,
                                         'user_account': self.first_account.pk,
                                         'nominal_value':'20000.00',
                                         'interest_type':1,
                                         'interest_rate':'7.50', 
                                         'ip_address': loan.ip_address,
                                         'request_date': request_date,
                                         'end_date': '2021-10-10',
                                         'bank':'BRB', 
                                         'client':'Jon Snow', 
                                         'full_debt': loan.get_full_debt, 
                                         'total_paid': loan.get_total_paid, 
                                         'outstanding_balance': loan.get_outstanding_balance})
        self.assertEqual(loan.user_account, self.first_account)
    
    def test_payment_put(self):
        data = {
            'loan': self.loan.pk, 
            'date': '2021-06-20',
            'value': 7000,
        }
        response = self.client.put(reverse('payment_detail', 
                                           args=[self.payment.pk]), 
                                   data)
        payment = Payment.objects.get(pk=self.payment.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': payment.pk,  
                                         'value':'7000.00', 
                                         'date': '2021-06-20', 
                                         'loan': payment.loan.pk})
    
    def test_payment_put_with_value_bigger_than_loan(self):
        data = {
            'loan': self.loan.pk, 
            'date': '2021-06-20',
            'value': 30000,
        }
        response = self.client.put(reverse('payment_detail', 
                                           args=[self.payment.pk]), 
                                   data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "The total paid needs to be less or equal than the full debt.")
    
    def test_payment_put_with_negative_value(self):
        data = {
            'loan': self.loan.pk, 
            'date': '2021-06-20',
            'value': -3000,
        }
        response = self.client.put(reverse('payment_detail', 
                                           args=[self.payment.pk]), 
                                   data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "The value needs to be greater than zero.")
    
    def test_payment_put_to_other_users_loan(self):
        data = {
            'loan': self.second_loan.pk, 
            'date': '2021-06-20',
            'value': 3000,
        }
        response = self.client.put(reverse('payment_detail', 
                                           args=[self.payment.pk]), 
                                   data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(response.data, 
                                 "You need to be the loan's user.")
    
    # Tests for DELETE requests
    def test_loan_delete(self):
        loans_length = Loan.objects.all().count()
        response = self.client.delete(reverse('loan_detail', 
                                           args=[self.loan.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Loan.objects.all().count(), loans_length-1)
    
    def test_payment_delete(self):
        payments_length = Payment.objects.all().count()
        response = self.client.delete(reverse('payment_detail', 
                                           args=[self.payment.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payment.objects.all().count(), payments_length-1)
        
        