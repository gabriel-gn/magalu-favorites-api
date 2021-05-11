from django.urls import path

from src.user_profile.views import *

app_name = 'user_profile'
urlpatterns = [
    # API REST
    path('auth', AuthToken.as_view(), name='auth'),
    path('register', RegisterUser.as_view(), name='register'),
]