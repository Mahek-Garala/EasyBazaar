from django.shortcuts import render
from .models import Category,Product
# Create your views here.
def home(request):
    categories = Category.objects.all()
    data = {
        "categories":categories
    }
    return render(request,'home.html',data)

def show_product(request,id):
    products = Product.objects.filter(category=id)
    data = {
        "products":products
    }
    return render(request,'category.html',data)
