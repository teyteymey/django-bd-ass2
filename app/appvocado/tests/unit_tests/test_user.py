import json
from lib2to3.pgen2 import token
from msilib.schema import File
import os
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests

from appvocado.models import Category, Offer, Reservation, Friends, FavoriteOffers

#test de endpoints related to the model Offer
class OffersTests(APITestCase):

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

    def test_create_offer_success(self):
        """
        Test the creation of offers
        """

        payload={
            'category_type': 'Fruits',
            'title': 'Kg of avocados',
            'description': 'I bought too many',
            'end_date': '2022-02-02'
        }

        files=[ #an example file, does not need to be accurate for it to test the endpoint
        ('image',('coconut_bars.jpg',open(os.path.join(self.test_root, 'coconut_bars.jpg'),'rb'),'image/png'))
        ]

        headers = {
        'Authorization': self.token
        }

        url = "http://127.0.0.1:8000/offers/"
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Kg of avocados')
        self.assertEqual(response.data['description'], 'I bought too many')