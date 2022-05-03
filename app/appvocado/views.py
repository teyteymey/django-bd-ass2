from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from appvocado.serializers import UserSerializer
from appvocado.serializers import ReservationSerializer
from appvocado.models import Reservation, Offer, Category, UserReview


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

# clears all the elements of offer, reservation and user in the database. It is useful for debugging
class clearDB(APIView):
    
    def get(self, request):
        users = User.objects.all()
        for user in users:
            user.delete()
        reservs = Reservation.objects.all()
        for res in reservs:
            res.delete()
        offers = Offer.objects.all()
        for offer in offers:
            offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# Displays a list of reservations in the system.
class ReservationList(APIView):

    def get(self, request, format=None):
        reservation = Reservation.objects.all()
        serializer = ReservationSerializer(reservation, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        #data = self.request.data
        #data['username'] = self.request.user.username
        #data['username'] = request.user.username
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):  #get, put and delete

    def get(self, request, username):       #only the user can request this
        #if not request.user.is_authenticated: raise NotAuthenticated
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = User.objects.get(username = username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        if username == request.user.username:
            user = User.objects.get(username = username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        Response({"Message": "You can only delete your own account!"},status=status.HTTP_401_UNAUTHORIZED)