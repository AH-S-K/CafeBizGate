from django.contrib import admin
from django.urls import path , include
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
]
