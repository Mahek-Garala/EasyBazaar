from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length= 50)
    phone = models.CharField(max_length = 10)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50) 
    def __str__(self):
        return self.name
