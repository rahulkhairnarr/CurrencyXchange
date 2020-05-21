from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from wallet.models import Wallet
from userprofiles.api.serializers import UserSerializer
from django.urls import reverse
import json


class CreateWalletTestCase(APITestCase):

    def setUp(self):
        self.username = 'admin3'
        self.password = '123456'
        self.email = "admin2@admin.com"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token, self.created = Token.objects.get_or_create(user=self.user)
    
    def test_registration(self):
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ str(self.token))
        response = self.client.get(path='/api/create_wallet/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadWalletTestCase(APITestCase):

    def setUp(self):
        self.username = 'admin3'
        self.password = '123456'
        self.email = "admin2@admin.com"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token, self.created = Token.objects.get_or_create(user=self.user)
        self.create_wallet()

    def create_wallet(self):
        self.wallet = Wallet.objects.create(user=self.user)

    
    def test_registration(self):
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ str(self.token))
        response = self.client.get(path='/api/get_balance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)