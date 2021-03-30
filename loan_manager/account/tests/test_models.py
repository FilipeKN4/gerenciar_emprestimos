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
    
    def test_user_creation(self):
        data = {
            'username': 'test_user', 
            'email': 'test_user@mail.com',
            'password': 'password123',
        }
        
        response = self.client.post('/account/accounts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)