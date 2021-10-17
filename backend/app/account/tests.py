from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework import status


# Create your tests here.

class Account(APITestCase):
    def setUp(self) -> None:
        user = User(username='test_user', email='test@gmail.com')
        user.set_password('test1234')
        user.save()

    def test_login_api(self):
        data = {
            'username': 'test_user',
            'password': 'test1234'
        }
        url = reverse('auth:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_api(self):
        data = {
            'username': 'new_test_user',
            'email': 'test01@gmai.com',
            'password': 'test1234'
        }
        url = reverse('auth:registration')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
