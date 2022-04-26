from rest_framework.decorators import api_view
from rest_framework.exceptions import *
from rest_framework.response import Response


mytoken = 'default'

#It is the home route, and lists the available calls
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'Clear database' : '/deletedb    #clears all the data in the database',
        
        'Create an account': '/register    #registers a new user',
        'Login': '/login    #login to be authorised',
        'Logout': '/logout',
        'Reset password' : '/reset_pass',
        'View my account' : '/user    #need to be logged in',
        'Delete my account' : 'user/<str:username>',

        
        'See and add reservations': 'user/<str:username>/reservations',
        'See and delete my reservation' : 'user/<str:username>/reservations/<int:id>',
        
        'See all rooms': '/rooms', #post, get
        'Search rooms by dates': '/rooms/?iniDate=date&?endDate=date',  #rooms/?endDate=2022-02-20&iniDate=2022-02-20
        'See free rooms in a date': '/rooms/?FreeIndate=date',

        'See room details': 'rooms/<str:code>', #get, put and delete
        'See all reservations': '/reservations    #for debugging purposes, it would not make sense it was public', #get and post

    }
    return Response(api_urls)
