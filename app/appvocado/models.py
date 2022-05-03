from django.db import models
from django.forms import CharField, DateField
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Offer(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, unique=False)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images/')
    closed = models.BooleanField()
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    closed_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

{
    "category_id": "1",
    "title" : "Kg of avocados",
    "description": "I bought too many",
    "image" : "",
    "end_date": "",
}

class Reservation(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user_id', 'offer_id'], name='unique_user_offer'),
        ]
    
        def __str__(self):
            return 'offer: ' + self.user_id + ' user: ' + self.offer_id


class UserReview(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer_id = models.IntegerField()
    rating = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user_id', 'reviewer_id'], name='unique_review'),
        ]
    
        def __str__(self):
            return 'user_id: ' + self.user_id + ' reviewer_id: ' + self.reviewer_id + ' rating: ' + self.rating