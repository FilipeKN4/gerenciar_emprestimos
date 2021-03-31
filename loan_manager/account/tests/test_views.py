# Rest Framework imports
from rest_framework import status
from rest_framework.test import APITestCase

# Account app imports
from account.models import Account


class TestAccount(APITestCase):
    def setUp(self):
        self.admin_account = Account.objects.create_superuser(
            username='teste',
            email='teste@mail.com',
            password='password123'
        )
        self.account = Account.objects.create_user(
            username='jon',
            email='jon@mail.com',
            password='password123'
        )
        self.login()
    
    def login(self):
        self.client.force_authenticate(self.admin_account)
        
    def test_user_login(self):
        self.client.logout()
        response = self.client.post('/login/', {'username': 'teste@mail.com', 
                                                'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Tests for GET requests
    def test_accounts_list(self): 
        response = self.client.get('/account/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_accounts_get(self): 
        response = self.client.get('/account/accounts/{}/'.format(self.account.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Tests for POST and PUT requests
    def test_account_post(self):
        accounts_length = Account.objects.all().count()
        data = {
            'username': 'test_user', 
            'email': 'test_user@mail.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        
        response = self.client.post('/account/accounts/', data)
        last_account = Account.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': last_account.id, 
                                         'email': 'test_user@mail.com',
                                         'username': 'test_user', 
                                         'first_name': 'Test',
                                         'last_name': 'User',
                                         'is_admin': False, 
                                         'is_active': True, 
                                         'is_staff': False, 
                                         'is_superuser': False}) 
        self.assertEqual(Account.objects.all().count(), accounts_length+1)
        
    def test_account_put(self):    
        data = {
            'username': 'jon_snow', 
            'email': 'jon_snow@mail.com',
            'password': '123',
            'first_name': 'Jon',
            'last_name': 'Snow',
            'is_active': True
        }
          
        response = self.client.put('/account/accounts/{}/'.format(self.account.id), 
                                   data)
        last_account = Account.objects.last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': last_account.id, 
                                         'email': 'jon_snow@mail.com',
                                         'username': 'jon_snow', 
                                         'first_name': 'Jon',
                                         'last_name': 'Snow',
                                         'is_admin': False, 
                                         'is_active': True, 
                                         'is_staff': False, 
                                         'is_superuser': False})
        
    # Tests for DELETE requests
    def test_account_delete(self):
        accounts_length = Account.objects.all().count()
        response = self.client.delete('/account/accounts/{}/'.format(self.account.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.all().count(), accounts_length-1)