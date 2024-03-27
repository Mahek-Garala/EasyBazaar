from django.shortcuts import get_object_or_404, render,redirect
from .models import Category,Product,Seller , Wishlist , Customer
from signup_login import views
from django.http import HttpResponse, JsonResponse

# Create your views here.

def home(request):
    categories = Category.objects.all()
    data = {
        "categories":categories
    }
    return render(request,'home.html',data)

#///////////////////////////////////////////////////////////////////////////////////////////////

def show_product(request, category_id):
    products = Product.objects.filter(category=category_id)

    customer_id = request.session.get('cust_id')

    product_wishlist_info = {}

    if customer_id:
        wishlist_items = Wishlist.objects.filter(customer_id=customer_id)

        wishlist_product_ids = set(item.product_id for item in wishlist_items)

        for product in products:
            is_in_wishlist = product.id in wishlist_product_ids
            product_wishlist_info[product.id] = is_in_wishlist

    data = {
        "products": products,
        "product_wishlist_info": product_wishlist_info
    }
    return render(request, 'category.html', data)


#//////////////////////////////////////////////////////////////////////////////////////////////

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

        products = Product.objects.filter(seller_id = request.session['id'])
        data = {
            "products":products
        }
        return render(request , 'seller_home.html' , data ) 
    products = Product.objects.filter(id=product_id)
    data = {
        "products":products
    }
    return render(request, 'update.html', data )

#//////////////////////////////////////////////////////////////////////////////////////////////


def delete_product(request , product_id):
   product = get_object_or_404(Product, id=product_id)
   product.delete()
   return redirect('seller_home') 


#//////////////////////////////////////////////////////////////////////////////////////////////



def add_product(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        stock = request.POST.get('stock')
        availability = request.POST.get('availability') == 'available'
        subcategory = request.POST.get('subcategory')
        image = request.FILES.get('image')
        

        seller_id = request.session.get('id')

        seller = Seller.objects.get(id = seller_id)
        category = Category.objects.get(name = category_name)
        # Create new Product instance
        new_product = Product(
            name=name,
            price=price,
            description=description,
            category= category,
            stock=stock,
            seller_id = seller , 
            available=availability,
            subcategory=subcategory,
            image=image
        )
        new_product.save()

        return redirect('seller_home')

    return render(request, 'add_product.html')


#//////////////////////////////////////////////////////////////////////////////////////////////


def seller_home(request):
    products = Product.objects.filter(seller_id = request.session.get('id') )
    data = {
            "products":products,
            "seller_id" : request.session.get('id') 
    }
    return render(request , 'seller_home.html' , data)


#//////////////////////////////////////////////////////////////////////////////////////////////


def wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, id=request.session.get('cust_id'))
    cat=product.category
    cat_id=cat.id

    in_wishlist = Wishlist.objects.filter(product=product, customer=customer).exists()
    if not in_wishlist:
        new_wishlist = Wishlist(product=product, customer=customer)
        new_wishlist.save()

    products = Product.objects.filter(category=cat_id)
    data = {
        "products":products,
        "in_wishlist": in_wishlist
    }
    return render(request,'category.html',data)

    
#//////////////////////////////////////////////////////////////////////////////////////////////


def wishlist_view(request):

    cust_id = request.session.get('cust_id')
    customer = Customer(id = cust_id)
    products = Wishlist.objects.filter(customer = customer) 
   
    return render(request , 'wishlist.html' , {'products' : products})


#//////////////////////////////////////////////////////////////////////////////////////////////


def remove_from_wishlist(request , product_id):

    cust_id = request.session.get('cust_id')
    customer = Customer(id = cust_id)
    product = Product(id = product_id)
    products = Wishlist.objects.filter(customer = customer , product = product)
    remaining_products = Wishlist.objects.filter(customer = customer)

    products.delete()
    return render(request , 'wishlist.html' , {'products' : remaining_products})