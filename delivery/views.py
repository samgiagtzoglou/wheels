from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import *
from models import Buyer, Restaurant, Order, FoodItem, Quantities
from django.shortcuts import redirect

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
            itemsInCart = current_order.cartlist
            quants = Quantities.objects.get(order=current_order)

            cart = []
            total = 0.00
            for it in itemsInCart:
                q = Quantities.objects.get(order=current_order,foodItem=it)
                if q.quantity > 0:
                    cart.append({'name':it.name, 'price':it.price, 'quantity':q.quantity, 'id':it.id})
                    total = total + (it.price * q.quantity)
        else:
            cart = []
        restaurants = Restaurant.objects.all()
        items = FoodItem.objects.all()
        return render(request, 'browse.html', {'itemsInCart' : cart, 'restaurants' : restaurants, 'items' : items, 'total' : total})

@login_required
def addItemToCart(request, item_id):
    item = FoodItem.objects.get(id=item_id)
    order = request.user.buyer.current_order
    if order == None:
        o = Order(user=request.user)
        o.save()
        quant = Quantities.objects.create(order=o,foodItem=item,quantity=1)
        quant.save()
        request.user.buyer.current_order = o
        request.user.buyer.save()
    else:   
        i = Quantities.objects.get(order=order,foodItem=item)
        i.quantity = i.quantity + 1
        i.save()
    return redirect('browse')

@login_required
def removeItemFromCart(request, item_id):
    item = FoodItem.objects.get(id=item_id)
    order = request.user.buyer.current_order
    if order == None:
        pass #throw an error maybe
    else:   
        i = Quantities.objects.get(order=order,foodItem=item)
        i.quantity = i.quantity - 1
        i.save()
    return redirect('browse')

@login_required
def checkout(request):
    pass #checkout 
