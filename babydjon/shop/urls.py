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
    path('addresses/', views.addresses, name = "addresses"),
    path('cart/deleteOneProductFromCart/', views.deleteOneProductFromCart, name = "deleteOneProductFromCart"),
    path('cart/deleteProductsFromCart/', views.deleteProductsFromCart, name = "deleteProductsFromCart"),
    path('cart/updateCost/', views.updateCost, name = "updateCost"),
    path('cart/updateCountInCart/', views.updateCountInCart, name = "updateCountInCart")
]