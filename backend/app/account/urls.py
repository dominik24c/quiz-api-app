from django.urls import path
from .api import RegisterApi, LoginApi

urlpatterns = [
    path('auth/register', RegisterApi.as_view(), name='registration'),
    path('auth/login', LoginApi.as_view(), name='login'),
]
