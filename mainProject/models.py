from django.db import models
from signup_login.models import Seller , Customer
# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='uploads/categories')
    desciption = models.TextField(max_length=200, default='', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    description = models.TextField(max_length=200, default='', null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    subcategory = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.name
    


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Wishlist-{self.id}"


