from django.contrib import admin
from django.urls import path
import shop.views  as views

urlpatterns = [
    path('', views.index, name = "home"),
    path('product/<int:productid>', views.product, name = "product"),
    path('profile/', views.profile, name = "profile"),
    path('login/', views.login, name = "login"),
    path('register/', views.registration, name = "register"),
    path('cart/', views.cart, name = "cart"),
    path('orders/', views.orders, name = "orders"),
    path('addresses/', views.addresses, name = "addresses")
]
