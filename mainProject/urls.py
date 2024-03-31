from django.contrib import admin
from django.urls import path , include
# from signup_login import views 
from . import views;
urlpatterns = [
    path('',views.home , name = 'home'),
    path('category/<int:category_id>/', views.show_product, name='show_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('addProduct/' , views.add_product , name = 'add_product'),
    path('seller_home/' , views.seller_home , name = 'seller_home'),
    path('wishlist/<int:product_id>/' , views.wishlist , name = 'wishlist' ),
    path('wishlist_view/' , views.wishlist_view , name = 'wishlist_view'),
    path('remove_wishlist/<int:product_id>' , views.remove_from_wishlist , name = 'remove_from_wishlist'),
    path('cart/<int:product_id>/' , views.cart , name = 'cart' ),
    path('cart_view/' , views.cart_view , name = 'cart_view'),
    path('remove_from_cart/<int:product_id> ' , views.remove_from_cart , name = 'remove_from_cart'),
    path('increase/<int:product_id>', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('buyProduct/' , views.buyProduct , name = 'buyProduct'),
    path('payment/' , views.payment , name = 'payment'),
    path('order_view/' , views.order_view , name = 'order_view'),
    path('admin_site/', views.admin_site , name = 'admin_site'),
    path('product_analysis/' , views.product_ana , name = 'product_ana'),
    path('category_analysis/' , views.category_ana , name = 'category_ana'),
    path('user_analysis/' , views.user_ana , name = 'user_ana'),
    path('seller_analysis/' , views.seller_ana , name = 'seller_ana'),
    path('remove_product/<int:product_id>/' , views.remove_product , name = 'remove_product') , 
    path('remove_category/<int:category_id>/' , views.remove_category , name = 'remove_category'),
    path('remove_user/<int:user_id>/' , views.remove_user , name = 'remove_user'),
    path('remove_seller/<int:seller_id>/' , views.remove_seller , name = 'remove_seller'),
    path('add_category/' , views.add_category , name = 'add_category'),
    path('profile/' , views.profile_view , name = 'profile_view') ,
    path('admin_home/' , views.admin_home , name = 'admin_home') , 
    path('admin_home/' , views.admin_home , name = 'admin_home') , 
    path('profile_seller/' , views.profile_seller , name = 'profile_seller') , 
    path('seller_sales/',views.seller_sales , name = 'seller_sales')

]



