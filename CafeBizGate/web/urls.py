from django.contrib import admin
from django.urls import path , include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('users/', views.user_list, name='user-list'),
    path('delete-user/', views.delete_user, name='delete-user'),
    path('login/', views.login_view, name='login'),
    path('management/' , views.management_view , name='management'),
    path('management/manage-inventory/', views.manage_inventory, name='manage_inventory'),
    path('unauthorized/' , views.unauthorized_access , name='unauthorized'),
    path('management/add_product/', views.add_product, name='add_product'),
    path('api/sales-data/', sales_data, name='sales-data'),
    path('api/products/', views.product_list, name='product_list'),
    path('products/', views.display_products, name='products'),
    path('products/<str:category>/', views.display_products, name='products_with_category'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('order_history/', views.order_history, name='order_history'),
    path('clear-cart/' , views.clear_cart , name='clear-cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-purchase-history/', clear_purchase_history, name='clear_purchase_history'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

