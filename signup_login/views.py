from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .models import Customer
from .models import Seller

from mainProject.models import Category,Product
from django.contrib.auth.hashers import make_password , check_password

# Create your views here.


def signup(request):

    if request.method == 'POST':
        type  = request.POST.get('type')
        name = request.POST.get('name')
        email  = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        existing_customer = None
        existing_seller = None
        if type == "Customer" : 
            existing_customer = Customer.objects.filter(email=email).first() 
        elif type == "Seller" :
            existing_seller = Seller.objects.filter(email=email).first() 

        data = {
            "error_message": "",
            "page" : "signup",
            "name" : name,
            "email" : email,
            "password" : password,
            "phone" : phone,
            "type" : type,
        }
        if existing_customer or existing_seller:
            data['error_message']= "User with the same email is already exist"
            return render(request,'login.html',data)
        if len(password) < 8:
            data["error_message"] = "Password should have at least 8 character"
            return render(request, 'login.html', data)
        if len(phone) != 10:
            data["error_message"] = "Phone number should be 10 digits"
            return render(request, 'login.html', data)
        
    
        
        if type == "Customer" :

            customer = Customer(name=name, email=email, phone=phone, password=password)
            customer.password = make_password(customer.password)
            customer.save()

        elif type == "Seller" :
            # company_name = request.POST.get('company_name')
            # data['company_name'] = company_name
            # seller = Seller(name=name, email=email, phone=phone, password=password,company_name="XYZ")
            # seller.password = make_password(seller.password)
            # seller.save()
            # data['page'] = "seller_auth"
            request.session['data'] = data 
            return redirect ('seller_auth')
            # return render(request,'company.html',data)

        data['page'] = "login"

    return render(request,'login.html')

def seller_auth(request):
    if request.method == 'POST':
        data = request.session.get('data')
        name = data['name']
        email  = data['email']
        password = data['password']
        phone = data['phone']
        company_name = request.POST.get('companyName')
        image = request.POST.get('companyProof')
        seller = Seller(name=name, email=email, phone=phone, password=password,company_name=company_name,proof_img=image)
        seller.password = make_password(seller.password)
        seller.save()

        products = Product.objects.filter(seller_id = seller.id )
        data = {
            "products":products
        }
        # request.session.pop('data', None)
        return render(request,'seller_home.html' , data)
     
    return render(request,'company.html')


def login(request):
    data = {
        "error_message": "",
        "page": "login",
        "name": "",
        "password": "",
    }
   
    if request.method == 'POST':
        type  = request.POST.get('type')
        name = request.POST.get('name')
        password = request.POST.get('password')
        flag = True
        customer = None
        seller = None
        try:
            if type == "Customer" :
                customer = Customer.objects.get(name=name)
            elif type == "Seller" :
                seller = Seller.objects.get(name=name)
        except:
            flag = False

        

        if customer and type == "Customer"  :
            flag = check_password(password,customer.password)
            if flag:
                # return render(request,'home.html')
                request.session['customer'] = customer.id
                return redirect('/home/')
            
        if seller and type == "Seller":
            flag = check_password(password,seller.password)
            if flag:
                request.session['seller'] = seller.id
                products = Product.objects.filter(seller_id = seller.id )
                data = {
                    "products" : products
                }
                return render(request,'seller_home.html',data)

        
        data["error_message"] = "Invalid Username or Password"
        data["name"] = name
        data["password"] = password
    return render(request,'login.html',data)