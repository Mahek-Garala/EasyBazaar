from django.contrib import admin
from django.urls import path , include
# from signup_login import views 
from . import views;
urlpatterns = [
    path('',views.home , name = 'home'),
    path('category/<int:id>/',views.show_product,name='show_product')
]



