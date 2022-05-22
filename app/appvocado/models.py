from django.db import models
from django.forms import CharField, DateField
from django.contrib.auth.models import User
from django.conf import settings

#Model of Category
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

# Model of Offer
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

# Model of reservation
class Reservation(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user_id', 'offer_id'], name='unique_user_offer'),
        ]
    
        def __str__(self):
            return 'user: ' + self.user_id + ' offer: ' + self.offer_id

# We do not really use it
#Model of user Review
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

# Model of Friends
# Has a uniqueness constraint.
class Friends(models.Model):
    user_id_1 = models.IntegerField();
    user_id_2 = models.IntegerField();

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user_id_1', 'user_id_2'], name='unique_friends'),
        ]
    
        def __str__(self):
            return 'user_id_1: ' + self.user_id_1 + ' user_id_2: ' + self.user_id_2

# Model of Favorite Offers
# Has a constraint of uniqueness so we can only favorite once an offer
class FavoriteOffers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user_id', 'offer_id'], name='unique_favorite_offer'),
        ]
    
        def __str__(self):
            return 'user: ' + self.user_id + ' offer: ' + self.offer_id