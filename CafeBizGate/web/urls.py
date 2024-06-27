from django.contrib import admin
from django.urls import path , include
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('users/', views.user_list, name='user-list'),
    path('delete-user/', views.delete_user, name='delete-user'),
    path('delete-user2/', views.delete_user2, name='delete-user2'),
    path('management/' , views.management_view , name='management'),
    path('management/manage-inventory/', views.manage_inventory, name='manage_inventory'),
    path('management/add_product/', views.add_product, name='add_product'),
    path('unauthorized/' , views.unauthorized_access , name='unauthorized'),

]

#برای اضافه  شدن عکس به دیتا بیس
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
