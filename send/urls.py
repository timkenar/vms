from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('api/send/mail', Sendmail.as_view())
]