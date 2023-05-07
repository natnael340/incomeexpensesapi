from rest_framework.test import APITestCase, APIClient 
from django.urls import reverse

class TestSetUp(APITestCase):
    

    def setUp(self) -> None:
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
        self.user_data = {
            'email': 'm4lik147@gmail.com',
            'username': 'm4lik147',
            'password': 'password',
        }


        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()