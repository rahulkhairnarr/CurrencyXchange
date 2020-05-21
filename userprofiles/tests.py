from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
import json


class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.username = 'admin3'
        self.password = '123456'
        self.email = "admin2@admin.com"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token, self.created = Token.objects.get_or_create(user=self.user)
    
    def test_registration(self):
        data = {'username': 'test_user5','password': '123456','email': 'test_user15@gmail.com'}
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ str(self.token))
        response = self.client.post(path='/api/registration/',data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.username = 'test_user5'
        self.password = '123456'
        self.email = "admin2@admin.com"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token, self.created = Token.objects.get_or_create(user=self.user)
    
    def test_login(self):
        data = {'username': 'test_user5','password': '123456'}
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ str(self.token))
        response = self.client.post(path='/api/login/',data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
