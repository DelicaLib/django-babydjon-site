from django.contrib import admin
from django.urls import path
from shop.views import *

urlpatterns = [
    path('', index, name = "home"),
]
