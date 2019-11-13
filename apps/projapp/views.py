from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
import bcrypt
from .models import *
import urllib 
import json
import datetime
import copy
## currency API Key 
API_KEY = "2ced39897a3d1c0116edcbbbeb5d0d15"

#############################        HOME      ###############################

def index(request):
    return render(request,"projapp/home.html")

#############################        LOGIN     ###############################

def login(request): 
    return render(request, "projapp/login.html")

#############################       LOGOUT     ###############################

def logout(request):
    del request.session['user']
    return redirect("/")

#############################  LOGIN PROCESS   ###############################

def login_process(request):
    if (User.objects.filter(email=request.POST['email']).exists()):
        user = User.objects.filter(email=request.POST['email'])[0]
        if (bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
            request.session['id'] = user.id
            messages.success(request, "User successfully logged in")
            return redirect('/success')
        messages.success(request, "Password didn't match")
    return redirect('/login')

#############################    REGISTER     ###############################

def register(request): 
    return render(request, "projapp/register.html")

############################# REGISTER PROCESS  ###############################

def register_process(request):
    if request.method=="POST":
        print("-"*80)
        errors=User.objects.register_validator(request.POST)
        if len(errors)>0:
            for tag,error in errors.items():
                messages.error(request,error, extra_tags=tag)
            return redirect("/register")
        else:
            first_name=request.POST["first_name"]
            last_name=request.POST["last_name"]
            email=request.POST["email"]
            password=bcrypt.hashpw(request.POST["password"].encode(),bcrypt.gensalt()).decode()
            print(password)
            new_user=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
            request.session["user"]=new_user.id
            messages.success(request, "Successfully registered(or logged in)!")
            return redirect("/success")

#############################    SUCCESS   ###############################

def success(request):
    context = {
            "user": User.objects.get(id = request.session['id']),
            "items": Item.objects.all()
            }
    return render(request,"projapp/success.html", context)

#############################   CREATE        #############################

def create(request):
    return render(request,"projapp/create.html")

#############################   CURRENCY       #############################

def currency(request):
    with urllib.request.urlopen("http://data.fixer.io/api/latest?access_key="+API_KEY) as url:
        data = json.loads(url.read().decode())
        rates = data["rates"]
        context = {
            "user": User.objects.get(id = request.session['id']),
            'rates': rates,
        }
    return render(request,"projapp/currency.html", context)

############################# CREATE PROCESS  ##############################

def create_process(request):
    user = User.objects.get(id = request.session['id'])
    newItem=Item.objects.create(title=request.POST['title'], description=request.POST['description'], price=request.POST['price'], uploaded_by = user)
    newItem.save()
    user.liked_items.add(newItem)
    return redirect("/success")

#################### ITEM SHOW ONE FUNCTION #####################

def showOne(request,id):                
    context = {
        "item": Item.objects.get(id=id),
        "items": Item.objects.all(),
        "user": User.objects.get(id = request.session['id'])
        }
    return render(request, "projapp/showOne.html", context)

#################### ITEM CHECKOUT FUNCTION #####################

def checkOut(request,id):                
    context = {
        "item": Item.objects.get(id=id),
        "items": Item.objects.all(),
        "user": User.objects.get(id = request.session['id'])
        }
    return render(request, "projapp/checkOut.html", context)

#################### CHECKOUT PAGE          #####################

def checkOutPage(request):
    return render(request,"projapp/checkout.html")

#################### SEARCH FUNCTION AJAX #####################

def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['srch']
    else:
        search_text = ''
    context = {
        "user": User.objects.get(id = request.session['id']),
        'items' : Item.objects.filter(title__contains=search_text)
    }
    return render(request,"projapp/success.html", context)