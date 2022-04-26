from django.urls import path
from . import views
from django.urls import path #re_path
# from dj_rest_auth.registration.views import RegisterView
# from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordChangeView

urlpatterns = [
    path('', views.ApiOverview, name='home')
]