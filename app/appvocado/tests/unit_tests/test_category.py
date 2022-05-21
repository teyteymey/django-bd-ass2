import json
from lib2to3.pgen2 import token
from msilib.schema import File
import os
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests
from django.test import Client

from appvocado.models import Category, Offer, Reservation, Friends, FavoriteOffers

#test the endpoints related to the model Category
class CategoryTests(APITestCase):
    token = 'def'
    test_root = 'def'
     
    # We need to set up the user and authorisation because most of the calls need of a token.
    def setUp(self):
        #self.client = Client()
        #User.objects.create(username="test", password1="test1234", password2="test1234", first_name = "test", last_name = "test")
        url = reverse('register')
        self.client.post(url, {'username': 'test', 'password1': 'test1234', 'password2': 'test1234', 'first_name' : 'test', 'last_name' : 'test'})
        url = reverse('login')
        response = self.client.post(url, {'username': 'test', 'password': 'test1234'})
        self.token = response.json()['access_token']
        self.token = 'Bearer '+ self.token #set up the token in the call
        self.test_root = os.path.abspath(os.path.dirname(__file__))
        
    # Create a category succesfully.
    def test_create_category_success(self):

        url = "http://127.0.0.1:8000/categories/"

        payload={'name': 'Fruits', 'description': 'Fruits'}
        files=[
        ('image',('coconut_bars.jpg',open(os.path.join(self.test_root, 'coconut_bars.jpg'),'rb'),'image/png'))
        ]

        headers = {
        'Authorization': self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Success")



    def test_create_category_failure_bad_request(self):
        """
        Failed creation of category because no image was added.
        """

        requestBody = {
            "name": "Success",
            "description": "Success",
        }

        file = {
            "image": open(os.path.join(self.test_root, "coconut_bars.jpg"), 'rb')
        }
        
        url = reverse('view_categories')
        response = self.client.post(url, data=requestBody, headers=token, files = file)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_failure_duplicate(self):
        """
        Test that there is not two categories with the same name
        """

        url = "http://127.0.0.1:8000/categories/"

        payload={'name': 'Fruits', 'description': 'Fruits'}
        files=[
        ('image',('coconut_bars.jpg',open(os.path.join(self.test_root, 'coconut_bars.jpg'),'rb'),'image/png'))
        ]

        headers = {
        'Authorization': self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        response = requests.request("POST", url, headers=headers, data=payload, files=files) #we send it twice so its repeated

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_category_list_success(self):
        """
        Get list of categories
        """

        url = "http://127.0.0.1:8000/categories/"

        payload={}
        headers = {
        'Authorization': self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_retrieve_category_detail_success(self):
        """
        Check details of a category are accurate.
        """

        url = "http://127.0.0.1:8000/categories/1"

        payload={}
        headers = {
        'Authorization': self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)


    def test_retrieve_category_detail_not_found(self):
        """
        Check that a category does not exist
        """
        
        url = "http://127.0.0.1:8000/categories/4040"

        payload={}
        headers = {
        'Authorization': self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)