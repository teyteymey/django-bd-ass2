from rest_framework import serializers
from django.contrib.auth.models import User

from appvocado.models import Category, Offer, Reservation, UserReview, Friends, FavoriteOffers

from dj_rest_auth.registration.serializers import RegisterSerializer

# Serializer to register user adding first and last names
class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }

# Serializer to create or edit an object of Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'image')

# Serializer to create or edit an object of Offer
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'category_id', 'user_id', 'title', 'description', 'image', 'closed', 'end_date', 'created_at', 'closed_at')

# Serializer to create or edit an object of Reservation
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'user_id', 'offer_id', 'accepted')

# Serializer to create or edit an object of UserReview
#In this case, it fell out of scope of the project
class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ('id', 'user_id', 'reviewer_id', 'rating')

# Serializer to create or edit an object of Friends
class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ('id', 'user_id_1', 'user_id_2')

# Serializer to create or edit an object of User
# The User used is the one provided by django authorisation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Serializer to create or edit an object of Favorite Offer
class FavoriteOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteOffers
        fields = ('id', 'user_id', 'offer_id')