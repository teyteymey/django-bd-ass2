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
class friendTests(APITestCase):

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

    # RS3 requirement
    def test_add_friend_success(self):
        """
        Test that we can add a new friend to the logged in user
        """

        payload = json.dumps({
            "user_id_2": 2
        })

        headers = {
        'Authorization': self.token
        }

        url = "http://127.0.0.1:8000/user/friends"
        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_see_friends_success(self):
        """
        Test the edit of the atributes of the logged user
        """

        payload = {}

        headers = {
        'Authorization': self.token
        }

        url = "http://127.0.0.1:8000/user/friends"
        response = requests.request("GET", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

