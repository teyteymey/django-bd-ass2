
import re
from unicodedata import category
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from appvocado.models import FavoriteOffers
from appvocado.serializers import FavoriteOfferSerializer
from appvocado.serializers import ReservationSerializer, OfferSerializer, UserSerializer, CustomRegisterSerializer, CategorySerializer, FriendsSerializer
from appvocado.models import Reservation, Offer, Category, UserReview, Friends


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

# clears all the elements of offer, reservation, category and user in the database. It is useful for debugging
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
        categories = Category.objects.all()
        for cat in categories:
            cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# Displays the list of reservations of the logged user in the system and allows to create a new one.
# Requires a user to be authenticated.
class ReservationList(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, format=None):
        reservation = Reservation.objects.all()
        serializer = ReservationSerializer(reservation, many=True)
        return Response(serializer.data)

    def post(self, request, format = None):
        try:
            offer_userId = Offer.objects.get(id = request.data["offer_id"]).user_id
        except:
            return Response({"Message": "The offer does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.id != offer_userId.id: #meaning it is not my own offer
            request.data["user_id"] = request.user.id
            serializer = ReservationSerializer(data=request.data)
            try:
                serializer.is_valid()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({"Message": "You already reserved this item"},status=status.HTTP_409_CONFLICT)
        return Response({"Message": "You can not reserve your own item."}, status=status.HTTP_400_BAD_REQUEST)

# Displays a list of offers in the system and allows to publish a new one.
# Requires a user to be logged in.
class OfferList(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, format=None):
        offer = Offer.objects.all()
        serializer = OfferSerializer(offer, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data["user_id"] = request.user.id
        request.data["category_id"] = Category.objects.get(name = request.data["category_type"]).id
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Allows a user to see the data of another user.
# Requires a user to be logged in.
class FriendDetail(APIView):  #get
    permission_classes = [IsAuthenticated] 

    def get(self, request, id):
        user = User.objects.get(id = id)
        serializer = CustomRegisterSerializer(user)
        return Response(serializer.data)  

#Allows the user to see its details, edit them and delete its account.
# Requires a user to be logged in.
class UserDetail(APIView):  #get, put and delete
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        serializer = CustomRegisterSerializer(request.user)
        return Response(serializer.data)  


    def put(self, request):
        fn = self.request.data.get('first_name')
        ln = self.request.data.get('last_name')
        email = self.request.data.get('email')
        User.objects.filter(username = request.user.username).update(first_name=fn, last_name = ln, email = email)
        return Response (status = status.HTTP_200_OK)

    def delete(self, request):
        user = User.objects.get(username = request.user.username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Returns de details of a reservation. Only authorised and logged in users can access this view, and only
# treat with reservations that are their own.
class ReservationDetail(APIView):      #/rooms/pk: get, put and delete

    def get(self, request, id, username):
        res = get_object_or_404(Reservation, id = id)
        resUsername= res.username.username.strip()  #because it had some white spaces and the comparison did not work
        if resUsername == request.user.username:   #if the user doing the call is the same of the reservation to see
            serializer = ReservationSerializer(res)
            return Response(serializer.data)
        else:
            return Response({"Message": "You can not see the reservation details of another user."},status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, id, username):
        res = get_object_or_404(Reservation, id = id)
        resUsername= res.username.username.strip()
        if resUsername == request.user.username:    #if the user doing the call is the same of the reservation to delete
            res.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Message": "You can not delete the reservation of another user."},status=status.HTTP_403_FORBIDDEN)

# Returns de details of an offer
class OfferDetails(APIView):
    def get(self, request, id):
        offer = get_object_or_404(Offer, id = id)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)

# Displays a list of categories in the system.
class CategoryList(APIView):

    def get(self, request, format=None):
        cat = Category.objects.all()
        serializer = CategorySerializer(cat, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Returns de details of an offer
class CategoryDetails(APIView):
    def get(self, request, id):
        cat = get_object_or_404(Category, id = id)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

# Returns all the requests for my offers
class OfferRequests(APIView):
    def get(self, request):
        wanted_items = set()
        for item in Offer.objects.filter(user_id = request.user.id):
            wanted_items.add(item.id)

        requests = Reservation.objects.filter(offer_id__in = wanted_items)
        serializer = ReservationSerializer(requests, many = True)
        return Response(serializer.data)

# Returns all the requests for my offers
class myOffers(APIView):
    def get(self, request):
        offers = Offer.objects.filter(user_id = request.user.id)
        serializer = OfferSerializer(offers, many = True)
        return Response(serializer.data)

# Returns all the friends of the logged in user and allows to add one new
class myFriends(APIView):
    def get(self, request):
        friends = Friends.objects.filter(Q(user_id_1 = request.user.id) | Q(user_id_2= request.user.id))    #library which allows to do an OR query
        serializer = FriendsSerializer(friends, many = True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data["user_id_1"] = request.user.id
        serializer = FriendsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Returns all the favorite offers of the logged user and allows to add a new one
class favoriteOffers(APIView):
    def get(self, request):
        fav_offers = FavoriteOffers.objects.filter(user_id = request.user.id)    #library which allows to do an OR query
        serializer = FavoriteOfferSerializer(fav_offers, many = True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data["user_id"] = request.user.id
        offer = Offer.objects.get(id = request.data["offer_id"])
        if offer.user_id.id == request.user.id:    # I can not add as a favorite one of my own offers
            return Response({"Message": "You can not add as a favorite one of your own offers."},status=status.HTTP_400_BAD_REQUEST)
        serializer = FavoriteOfferSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({"Message": "You already favorited this item"},status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Returns all the requests for my offers
class viewRequest(APIView):
    def get(self, request, id):
        wanted_items = set()
        for item in Offer.objects.filter(user_id = request.user.id):
            wanted_items.add(item.id)

        requests = Reservation.objects.filter(offer_id__in = wanted_items)
        try:
            request = get_object_or_404(requests, id = id)
        except:
            return Response({"Message": "You can not see the request of another user."},status=status.HTTP_403_FORBIDDEN)
        serializer = ReservationSerializer(request)
        return Response(serializer.data)
    
    def put(self, request, id):
        wanted_items = set()
        for item in Offer.objects.filter(user_id = request.user.id):
            wanted_items.add(item.id)

        requests = Reservation.objects.filter(offer_id__in = wanted_items)
        try:
            request = get_object_or_404(requests, id = id)
        except:
            return Response({"Message": "You can not accept the request of another user."},status=status.HTTP_403_FORBIDDEN)
        accepted = self.request.data.get('accepted')
        Reservation.objects.filter(id = id).update(accepted = accepted)
        return Response (status = status.HTTP_200_OK)