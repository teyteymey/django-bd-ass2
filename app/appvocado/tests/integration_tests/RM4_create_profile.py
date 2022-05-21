import json
from lib2to3.pgen2 import token
from msilib.schema import File
import os
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests

class test_RM4(APITestCase):

# Linked to requirement RM4
    def test_register_user(self):
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'test1234', 
            'password1': 'test1234', 
            'password2': 'test1234', 
            'first_name' : 'Marta', 
            'last_name' : 'Smith'
        })

        payload = {
            "email": "changemyemail@gmail.com",
            "first_name": "Marta",
            "last_name": "Smith"
        }

        headers = {
        'Authorization': response.json()['access_token']
        }

        url = "http://127.0.0.1:8000/user/"
        response = requests.request("PUT", url, headers=headers, data = payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)