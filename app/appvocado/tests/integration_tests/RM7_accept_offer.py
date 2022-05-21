import json
from lib2to3.pgen2 import token
from msilib.schema import File
import os
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests

class test_RM(APITestCase):

# Linked to requirement RM7
    def test_register_user(self):
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'test1234', 
            'password1': 'test1234', 
            'password2': 'test1234', 
            'first_name' : 'Marta', 
            'last_name' : 'Smith'
        })

        token = response.json()['access_token']

        url = "http://127.0.0.1:8000/user/requests"

        payload={}
        headers = {
        'Authorization': 'Bearer' + token,
        
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        offer_id =  response.json()[0]["id"]

        url = "http://127.0.0.1:8000/user/requests/" + offer_id

        payload={
            'accepted': 'true'
        }
        headers = {
        'Authorization': 'Bearer' + token,
        
        }

        response = requests.request("PUT", url, headers=headers, data=payload)