import json
from lib2to3.pgen2 import token
from msilib.schema import File
import os
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests

from appvocado.models import Category, Offer, Reservation, Friends, FavoriteOffers

#test de endpoints related to the model User
class userTests(APITestCase):

    token = 'def'
    test_root = 'def'
     
    # We need to set up the user and authorisation because most of the calls need of a token.
    def setUp(self):
        url = reverse('register')
        self.client.post(url, {'username': 'test', 'password1': 'test1234', 'password2': 'test1234', 'first_name' : 'test', 'last_name' : 'test'})
        url = reverse('login')
        response = self.client.post(url, {'username': 'test', 'password': 'test1234'})
        self.token = response.json()['access_token']
        self.token = 'Bearer '+ self.token #set up the token in the call
        self.test_root = os.path.abspath(os.path.dirname(__file__))
    
    def tearDown(self):
        url = reverse('logout')
        response = self.client.post(url)
        return super().tearDown()

    def test_details_user_success(self):
        """
        Test that we can see the details of the logged in user based on the logged in user
        """

        headers = {
        'Authorization': self.token
        }

        url = "http://127.0.0.1:8000/user/"
        response = requests.request("GET", url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #Linked to requirement RS8
    def test_put_details_user_success(self):
        """
        Test the edit of the atributes of the logged user
        """

        payload = {
            "email": "changemyemail@gmail.com",
            "first_name": "Marta",
            "last_name": "Smith"
        }

        headers = {
        'Authorization': self.token
        }

        url = "http://127.0.0.1:8000/user/"
        response = requests.request("PUT", url, headers=headers, data = payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_user_success(self):
        """
        Test the edit of the atributes of the logged user
        """
        headers = {
        'Authorization': self.token
        }

        url = "http://127.0.0.1:8000/user/"
        response = requests.request("DELETE", url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

