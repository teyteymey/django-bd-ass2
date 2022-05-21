
from msilib.schema import File
from rest_framework.test import APITestCase
from rest_framework import status
import requests
import json


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
        
        #self.assertEqual(response.content, json.dumps(expected_response_body))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_db(self):
        url = "http://127.0.0.1:8000/deletedb/"

        payload={}
    
        response = requests.request("GET", url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

