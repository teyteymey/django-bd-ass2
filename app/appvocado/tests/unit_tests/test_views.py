import json
from lib2to3.pgen2 import token
from msilib.schema import File
import os
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests

from appvocado.models import Category, Offer, Reservation, Friends, FavoriteOffers

#test the endpoints related to the model Category
class CategoryTests(APITestCase):
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

        print(response)
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


# Class to test the two general calls : they do not need authorisation
class GeneralTests(APITestCase):
    
    def test_get_endpoints(self):
        url = "http://127.0.0.1:8000/"

        payload={}
    
        response = requests.request("GET", url, data=payload)

        expected_response_body = {
            "Clear database": "/deletedb    #clears all the data in the database",
            "Create an account": "/register    #registers a new user",
            "Login": "/login    #login to be authorised",
            "Logout": "/logout",
            "Reset password": "/reset_pass",
            "View, edit and delete my account": "/user    #need to be logged in",
            "See another users profile": "/user/<int:id>",
            "See requests for my offers": "/user/requests",
            "See and accept a request for my offers": "/user/requests/<int:id>",
            "See my posted offers": "/user/offers",
            "See my friends": "/user/friends",
            "See my favorite offers": "/user/favorite_offers",
            "See and add reservations": "/reservations",
            "See categories": "/categories",
            "See category details": "/categories/<int:id>",
            "See and post offers": "/offers",
            "See offer details": "/offers/<int:id>"
        }
        print(response.content)
        self.assertEqual(response.content, expected_response_body)

    def test_delete_db(self):
        url = "http://127.0.0.1:8000/deletedb/"

        payload={}
    
        response = requests.request("GET", url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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


#     def test_create_offer_failure_bad_request(self):
#         """
#         TODO write documentation
#         """

#         username = 'user'
#         email = 'user@example.com'
#         password = 'SuperSecretPassword'
#         user = User.objects.create_user(username=username, email=email, password=password)

#         name = 'Test Category'
#         description = 'Test Category Description'
#         category = Category.objects.create(name=name, description=description)

#         requestBody = {
#             'category_id': category.id,
#             'user_id': user.id,
#             'name': 'Success',
#             'description': 'Success',
#             'closed': False,
#         }

#         url = reverse('offer-list')
#         response = self.client.post(url, requestBody, format='multipart')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
#     def test_create_offer_failure_duplicate(self):
#         """
#         TODO write documentation
#         """

#         username = 'user'
#         email = 'user@example.com'
#         password = 'SuperSecretPassword'
#         user = User.objects.create_user(username=username, email=email, password=password)

#         name = 'Test Category'
#         description = 'Test Category Description'
#         category = Category.objects.create(name=name, description=description)

#         requestBody = {
#             'category_id': category.id,
#             'user_id': user.id,
#             'name': 'Success',
#             'description': 'Success',
#             'closed': False,
#             'end_date': '2022-04-04T12:00:00Z',
#         }

#         url = reverse('offer-list')
#         self.client.post(url, requestBody, format='multipart')
#         response = self.client.post(url, requestBody, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
#     def test_retrieve_offer_list_success(self):
#         """
#         TODO write documentation
#         """

#         url = reverse('offer-list')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_retrieve_offer_detail_success(self):
#         """
#         TODO write documentation
#         """

#         username = 'user'
#         email = 'user@example.com'
#         password = 'SuperSecretPassword'
#         user = User.objects.create_user(username=username, email=email, password=password)

#         name = 'Test Category'
#         description = 'Test Category Description'
#         category = Category.objects.create(name=name, description=description)

#         requestBody = {
#             'category_id': category.id,
#             'user_id': user.id,
#             'name': 'Success',
#             'description': 'Success',
#             'closed': False,
#             'end_date': '2022-04-04T12:00:00Z',
#         }
#         response = self.client.post(reverse('offer-list'), requestBody, format='multipart')
#         expectedResponseBody = {
#             'id': 3,
#             'category_id': category.id,
#             'user_id': user.id,
#             'name': 'Success',
#             'description': 'Success',
#             'image': 'http://testserver/media/images/defaults/offer.png',
#             'closed': False,
#             'end_date': '2022-04-04T12:00:00Z',
#             'created_at': response.data.get('created_at'),
#             'closed_at': None
#         }
#         url = reverse('offer-detail', kwargs={"pk": 3})
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, expectedResponseBody)
    
#     def test_retrieve_offer_detail_not_found(self):
#         """
#         TODO write documentation
#         """
        
#         url = reverse('offer-detail', kwargs={"pk": 404})
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # def test_update_offer_success(self):
#     #     """
#     #     TODO write documentation
#     #     """

#     #     username = 'user'
#     #     email = 'user@example.com'
#     #     password = 'SuperSecretPassword'
#     #     user = User.objects.create_user(username=username, email=email, password=password)

#     #     name = 'Test Category'
#     #     description = 'Test Category Description'
#     #     category = Category.objects.create(name=name, description=description)

#     #     requestBody = {
#     #         'category_id': category.id,
#     #         'user_id': user.id,
#     #         'name': 'Success',
#     #         'description': 'Success',
#     #         'closed': False,
#     #         'end_date': '2022-04-04T12:00:00Z',
#     #     }
#     #     response = self.client.post(reverse('offer-list'), requestBody, format='multipart')
#     #     expectedResponseBody = {
#     #         'id': 3,
#     #         'category_id': category.id,
#     #         'user_id': user.id,
#     #         'name': 'Success',
#     #         'description': 'Success',
#     #         'image': 'http://testserver/media/images/defaults/offer.png',
#     #         'closed': False,
#     #         'end_date': '2022-04-04T12:00:00Z',
#     #         'created_at': response.data.get('created_at'),
#     #         'closed_at': None
#     #     }
#     #     response = self.client.post(reverse('category-list'), {'name': 'Success', 'description': 'Success'}, format='multipart')
#     #     # self.assertEqual(response.data, 1)
#     #     url = reverse('offer-detail', kwargs={"pk": 6})
#     #     response = self.client.put(url, data= {"name": "New name", "description": "New description"},format='multipart')
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data, expectedResponseBody)

#     def test_update_offer_bad_request(self):
#         """
#         TODO write documentation
#         """

#         username = 'user'
#         email = 'user@example.com'
#         password = 'SuperSecretPassword'
#         user = User.objects.create_user(username=username, email=email, password=password)

#         name = 'Test Category'
#         description = 'Test Category Description'
#         category = Category.objects.create(name=name, description=description)

#         requestBody = {
#             'category_id': category.id,
#             'user_id': user.id,
#             'name': 'Success',
#             'description': 'Success',
#             'closed': False,
#             'end_date': '2022-04-04T12:00:00Z',
#         }

#         response = self.client.post(reverse('offer-list'), requestBody, format='multipart')
#         url = reverse('offer-detail', kwargs={"pk": Offer.objects.get().id})
#         response = self.client.put(url, data= {"name": "New name"}, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_update_offer_not_found(self):
#         """
#         TODO write documentation
#         """

#         url = reverse('offer-detail', kwargs={"pk": 404})
#         response = self.client.put(url, data= {"name": "New name", "description": "New description"}, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # def test_delete_offer_success(self):
#     #     """
#     #     TODO write documentation
#     #     """

#     #     response = self.client.post(reverse('offer-list'), {'name': 'Success', 'description': 'Success'}, format='multipart')
#     #     # self.assertEqual(response.data, 1)
#     #     url = reverse('offer-detail', kwargs={"pk": 3})
#     #     response = self.client.delete(url, format='json')
#     #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_delete_offer_not_found(self):
#         """
#         TODO write documentation
#         """

#         url = reverse('offer-detail', kwargs={"pk": 404})
#         response = self.client.delete(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    