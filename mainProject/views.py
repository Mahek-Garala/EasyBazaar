from django.shortcuts import get_object_or_404, render,redirect
from .models import Category,Product,Seller , Wishlist , Customer , Cart , Order
from signup_login import views
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password , check_password

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

        wishlist_product_ids = set(item.product.id for item in wishlist_items)

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
    categories = Category.objects.all()
    data = {
        "categories":categories
    }
    return render(request, 'add_product.html' , data)


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


#//////////////////////////////////////////////////////////////////////////////////////////////

from django.http import JsonResponse

def product_suggestions(request):
    print("hello")
    if request.method == 'GET' and 'search' in request.GET:
        search_term = request.GET.get('search')
        print("Received search term:", search_term)
        try:
            products = Product.objects.filter(name__icontains=search_term)[:10]
            suggestions = [product.name for product in products]
            
            return JsonResponse({'suggestions': suggestions})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'error': 'An error occurred while fetching suggestions'}, status=500)
    else:
        return JsonResponse({'error': 'No search term provided or invalid request'}, status=400)

def product_show(request, product_name):
    print("product_show called")
    product = get_object_or_404(Product, name=product_name)
    data = {
        'products': [product]  # Wrap the product in a list
    }
    return render(request, 'product_show.html', data)

#//////////////////////////////////////////////////////////////////////////////////////////////
def cart(request , product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, id=request.session.get('cust_id'))
    cat=product.category
    cat_id=cat.id

    in_cart = Cart.objects.filter(product=product, customer=customer).exists()
    if not in_cart:
        new_cart = Cart(product=product, customer=customer)
        new_cart.stock += 1 
        new_cart.save()

    products = Product.objects.filter(category=cat_id)
    data = {
        "products":products,
        "in_cart": in_cart
    }
    return render(request,'category.html',data )

#//////////////////////////////////////////////////////////////////////////////////////////////


def cart_view(request):

    cust_id = request.session.get('cust_id')
    customer = Customer(id = cust_id)
    products = Cart.objects.filter(customer = customer) 
    total_price = sum(item.product.price * item.stock for item in products)
    data = { 
        
    }
   
    return render(request , 'cart.html' , {'products' : products , 'total_price' : total_price})

#//////////////////////////////////////////////////////////////////////////////////////////////


def remove_from_cart(request , product_id):

    cust_id = request.session.get('cust_id')
    customer = Customer(id = cust_id)
    product = Product(id = product_id)
    products = Cart.objects.filter(customer = customer , product = product)
    remaining_products = Cart.objects.filter(customer = customer)



    products.delete()
    cust_id = request.session.get('cust_id')
    customer = Customer(id = cust_id)
    products = Cart.objects.filter(customer = customer) 
    total_price = sum(item.product.price * item.stock for item in products)
    return render(request , 'cart.html' , {'products' : remaining_products , 'total_price' : total_price})

#///////////////////////////////////////////////////////////////////////////////////////////////////


def increase_quantity(request, product_id):
    cust_id = request.session.get('cust_id')
    product = get_object_or_404(Product, id = product_id)
    customer = get_object_or_404(Customer, id = cust_id)
    cart_item = get_object_or_404(Cart, product=product, customer = customer)
    cart_item.stock += 1
    cart_item.save()
    return redirect('cart_view')

def decrease_quantity(request, product_id):
    cust_id = request.session.get('cust_id')
    product = get_object_or_404(Product, id = product_id)
    customer = get_object_or_404(Customer, id = cust_id)
    cart_item = get_object_or_404(Cart, product=product, customer = customer)
    if cart_item.stock > 1:
        cart_item.stock -= 1
        cart_item.save()
    return redirect('cart_view')


#///////////////////////////////////////////////////////////////////////////////////////////////////


def buyProduct(request ):
    cust_id = request.session.get('cust_id')
    customer = get_object_or_404(Customer, id=cust_id)
    products = Cart.objects.filter(customer=customer) 

    data = { 
        "error_message": "",
        "products" : products , 
        "total_price" : ""
    }
    
    for cart_item in products:

        if cart_item.product.available != True:
            product = get_object_or_404(Product, id=cart_item.product.id)
            data['error_message'] = f"{product.name} is not available"
            return render(request, 'cart.html', data)
        elif cart_item.stock > cart_item.product.stock:
            product = get_object_or_404(Product, id=cart_item.product.id)
            data['error_message'] = f"{product.name}'s quantity is more than available stock"
            return render(request, 'cart.html', data)
        
    
    total_price = sum(item.product.price * item.stock for item in products)
    data['total_price'] = total_price 
    return render(request, 'payment.html' , data)  

#///////////////////////////////////////////////////////////////////////////////////////////////////


def payment(request):

    cust_id = request.session.get('cust_id')
    customer = get_object_or_404(Customer, id=cust_id)
    products = Cart.objects.filter(customer=customer) 
    total_price = sum(item.product.price * item.stock for item in products)

    for p in products:
        p.product.stock = p.product.stock -  p.stock
        p.product.save()
        product = get_object_or_404(Product, id= p.product.id)
        new_order = Order(product = product , customer = customer , quantity = p.stock )
        new_order.save()
        p.delete()

    products = Order.objects.filter(customer=customer) 



    data = {
        "products" : products

    }
    return render(request,'view_order.html', data)



#///////////////////////////////////////////////////////////////////////////////////////////////////

def order_view(request):

    cust_id = request.session.get('cust_id')
    customer = get_object_or_404(Customer, id=cust_id)

    products = Order.objects.filter(customer=customer) 
    data = {
        "products" : products

    }
    return render(request,'view_order.html', data)

#///////////////////////////////////////////////////////////////////////////////////////////////////

def admin_site(request):
    
    return render(request , 'admin.html' )


def product_ana(request):
    products = Product.objects.all()
    data = {
        "products":products    
    }
    return render(request , 'product_ana.html' , data)
    
def category_ana(request):
    category = Category.objects.all()
    data = {
        "category":category    
    }
    return render(request , 'category_ana.html' , data)

def user_ana(request):
    user = Customer.objects.all()
    data = {
        "user":user    
    }
    return render(request , 'user_ana.html' , data)

def seller_ana(request):
    seller = Seller.objects.all()
    data = {
        "seller":seller
    }
    return render(request , 'seller_ana.html' , data)

def remove_product(request , product_id):
    product = get_object_or_404(Product, id= product_id)
    product.delete()

    products = Product.objects.all()
    data = {
        "products":products    
    }
    return render(request , 'product_ana.html' , data)

def remove_category(request , category_id):
    category = get_object_or_404(Category, id= category_id)
    category.delete()

    category = Category.objects.all()
    data = {
        "category":category    
    }
    return render(request , 'category_ana.html' , data)

def remove_user(request , user_id):
    user = get_object_or_404(Customer, id= user_id)
    user.delete()
    users = Customer.objects.all()
    data = {
        "user":users   
    }
    return render(request , 'user_ana.html' , data)

def remove_seller(request , seller_id):
    seller = get_object_or_404(Seller, id= seller_id)
    seller.delete()
    sellers = Seller.objects.all()
    data = {
        "seller":sellers   
    }
    return render(request , 'seller_ana.html' , data)

def add_category(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        # Create new Product instance
        new_category = Category(
            name=name,
            description=description,
            photo=image
        )
        new_category.save()

        return render(request , 'admin.html')
    return render(request, 'add_category.html')


def profile_view(request):
    cust = request.session.get('cust_id')
    sell = request.session.get('id')

    data = {
        'user' : "" ,
        'type' : ""
    }
    if cust : 
        customer = get_object_or_404(Customer, id= cust)
        data['user'] = customer
        data['type'] = "Customer"

    elif sell :
        seller = get_object_or_404(Seller, id= sell)
        data['user'] = seller
        data['type'] = "Seller"

    return render(request , 'profile.html' , data)


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import check_password

