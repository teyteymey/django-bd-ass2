from django.urls import path, re_path
from . import views
from django.urls import path #re_path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordChangeView

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('deletedb/', views.clearDB.as_view()),
    path('register/', RegisterView.as_view(), name = 'register'), # do not insert an email, since it will want to confirm it
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view()),
    path('reset_pass/', PasswordChangeView.as_view()),
    path('user/', views.UserDetail.as_view()),
    path('user/<int:id>', views.FriendDetail.as_view()),
    path('reservations/', views.ReservationList.as_view(), name='view_reservations'),
    path('offers/', views.OfferList.as_view(), name='view_offers'),
    path('offers/<int:id>', views.OfferDetails.as_view(), name='view_offer_details'),
    path('categories/', views.CategoryList.as_view(), name='view_categories'),
    path('categories/<int:id>', views.CategoryDetails.as_view(), name='view_category_details'),
    path('user/requests', views.OfferRequests.as_view()),
    path('user/requests/<int:id>', views.viewRequest.as_view()), #accept it and see it
    path('user/offers', views.myOffers.as_view()),
    path('user/friends', views.myFriends.as_view()),
    path('user/favorite_offers', views.favoriteOffers.as_view()),
]