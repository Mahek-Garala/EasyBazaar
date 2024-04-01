from django.contrib import admin
from django.urls import path , include
# from signup_login import views 
from . import views;
urlpatterns = [
    path('',views.signup , name = 'signup'),
    path('login/' , views.login , name = 'login'),
    path('seller_auth/' , views.seller_auth , name='seller_auth'),
    path('logout/' , views.logoutpage , name = 'logoutpage'), 

]




