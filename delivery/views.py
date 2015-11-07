from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import *
from models import Buyer, Restaurant, Order, FoodItem


def home(request):
    return views.login(request)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Buyer.objects.create(user=user, current_order=None)
            return render(request, "registration/register_complete.html")
        return "Error"
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html',{'form':form})


@login_required
def browse(request):
    if request.method == 'GET':
        user = User.objects.get(username = request.user.username)
        if user.buyer.current_order != None:
            current_order = user.buyer.current_order
        else:
            current_order = Order(user=user)
            user.buyer.current_order = current_order
        restaurants = Restaurant.objects.all()
        items = FoodItem.objects.all()
        return render(request, 'browse.html', {'order' : current_order, 'restaurants' : restaurants, 'items' : items})

@login_required
def checkout(request):
    pass #checkout 

@login_required    
def addToCart(request):
    if request.method == 'POST':
        # form = 
        pass