from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.hashers import make_password , check_password

# Create your views here.

# def welcome(request):
#     return render(request,'welcome.html')
def signup(request):

    if request.method == 'POST':
        # type  = request.POST.get('type')
        name = request.POST.get('name')
        email  = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        existing_customer = Customer.objects.filter(email=email).first() 
        data = {
            "error_message": "",
            "page" : "signup",
        }
        if len(phone) != 10:
            data["error_message"] = "Phone number should be 10 digits"
            return render(request, 'login.html', data)
        if existing_customer:
            data['error_message']= "A customer with the same email already exists"
            return render(request,'login.html',data)
        customer = Customer(name=name, email=email, phone=phone, password=password)
        customer.password = make_password(customer.password)
        customer.save()
        data['page'] = "login"
    return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        type  = request.POST.get('type')
        name = request.POST.get('name')
        password = request.POST.get('password')
        flag = True
        try:
            customer = Customer.objects.get(name=name)
        except:
            flag = False
        print(customer)
        if customer:
            print(customer.password)
            flag = check_password(password,customer.password)
            print(flag)
            if flag:
                return render(request,'home.html')
        # customer = Customer.objects.filter(name=name, password=password).first()
        
        data = {
            "error_message": "Invalid Username or Password",
            "page" : "login",
        }
    return render(request,'login.html',data)