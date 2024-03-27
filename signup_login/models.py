from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 50)
    phone = models.CharField(max_length = 10)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50) 
    def __str__(self):
        return self.name
    
class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    company_name = models.CharField(max_length=255,null=True)
    proof_img = models.ImageField(upload_to='uploads/Seller/',null=True)

    def __str__(self):
        return self.name



