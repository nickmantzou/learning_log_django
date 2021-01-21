"""Defines URL patterns for users app"""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # include the default authorization url from django
    path('', include('django.contrib.auth.urls')),
    # Registration page
    path('register/', views.register, name='register'),
]