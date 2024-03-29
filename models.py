from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'



class Product(models.Model):
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
    


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    items = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return self.customer.name



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.quantity * self.product.price
    

    


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.IntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField('Product', through='OrderItem')

    def __str__(self):
        return self.customer.name
    


class OrderItem(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_item_price(self):
        return self.quantity * self.item_price
    
  

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'ShippingAddresses'

    def __str__(self):
        return self.customer.name



