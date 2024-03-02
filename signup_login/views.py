from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer
# Create your views here.

# def welcome(request):
#     return render(request,'welcome.html')
def signup(request):

    if request.method == 'POST':
        type  = request.POST.get('type')
        name = request.POST.get('name')
        email  = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        existing_customer = Customer.objects.filter(email=email).first() or Customer.objects.filter(phone=phone).first()
        if len(phone) != 10:
            return render(request, 'login.html', {'error_message': 'Phone number should be 10 digits'})
        if existing_customer:
            return render(request,'login.html',{'error_message': 'A customer with the same email or phone number already exists'})
        customer = Customer(name=name, email=email, phone=phone, password=password)
        customer.save()
        
    return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        type  = request.POST.get('type')
        name = request.POST.get('name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if len(phone) != 10:
            return render(request, 'login.html', {'error_message': 'Phone number should be 10 digits'})
        customer = Customer.objects.filter(name=name, password=password, phone=phone).first()
        if customer:
            return render(request,'home.html')
        
    return render(request,'login.html',{'error_message' : 'Username and Password does not match'})