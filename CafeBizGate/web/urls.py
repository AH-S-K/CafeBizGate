from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('products/', views.list_products, name='list_products'),
    path('products/create/', views.create_product, name='create_product'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/', views.view_order, name='view_order'),
    path('orders/', views.user_orders, name='user_orders'),
]

