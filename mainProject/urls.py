from django.contrib import admin
from django.urls import path , include
# from signup_login import views 
from . import views;
urlpatterns = [
    path('',views.home , name = 'home'),
    path('/category/<int:category_id>/', views.show_product, name='show_product'),
    path('/update/<int:product_id>/', views.update_product, name='update_product'),
    path('/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('addProduct/' , views.add_product , name = 'add_product'),
    path('/seller_home/' , views.seller_home , name = 'seller_home'),
    path('wishlist/<int:product_id>/' , views.wishlist , name = 'wishlist' ),
    path('/wishlist_view/' , views.wishlist_view , name = 'wishlist_view'),
    path('remove_wishlist/<int:product_id>' , views.remove_from_wishlist , name = 'remove_from_wishlist')
]



