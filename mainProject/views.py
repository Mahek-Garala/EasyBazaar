from django.shortcuts import render,redirect
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


def update_product(request, product_id):

    if request.method == 'POST':
        p = Product.objects.get(id=product_id)
        p.name = request.POST.get('name')
        p.price = request.POST.get('price')
        p.description = request.POST.get('description')
        p.categoryategory = request.POST.get('category')
        p.stock = request.POST.get('stock')
        p.availability = request.POST.get('availability')
        p.subcategory = request.POST.get('subcategory')
        p.save()
        return redirect('seller_home') 
    products = Product.objects.filter(id=product_id)
    data = {
        "products":products
    }
    return render(request, 'update.html', data )

def seller_home(request):
    return render(request , 'seller_home.html')

