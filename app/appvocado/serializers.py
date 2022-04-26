from rest_framework import serializers

from appvocado.models import Category, Offer, Reservation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'image')

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'category_id', 'user_id', 'name', 'description', 'image', 'closed', 'end_date', 'created_at', 'closed_at')

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'user_id', 'offer_id', 'accepted')
