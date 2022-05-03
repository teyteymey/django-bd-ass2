from django.urls import path, re_path
from . import views
from django.urls import path #re_path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordChangeView

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('deletedb/', views.clearDB.as_view()),
    path('register/', RegisterView.as_view()), # do not insert an email, since it will want to confirm it
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset_pass/', PasswordChangeView.as_view()),
    path('user/', views.UserDetail.as_view()),
    path('reservations/', views.ReservationList.as_view(), name='view_reservations'),
    path('offers/', views.ReservationList.as_view(), name='view_offers'),
]