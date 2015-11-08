from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import BuyerCreateForm, CarrierCreateForm
from models import Buyer, Carrier, Restaurant, Order, FoodItem, Quantities
from django.shortcuts import redirect

def home(request):
    return views.login(request)

def login(request):
    user = User.objects.get(username = request.user.username)
    if user.buyer:
        x = views.login(request)
        return "Carrier logged in"
    return x

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Buyer.objects.create(user=user, current_order=None, email=form.cleaned_data['email'])
            return render(request, "registration/register_complete.html")
        return "Error"
    else:
        form = BuyerCreateForm()
        return render(request, 'registration/register.html',{'form':form})

def register_carrier(request):
    if request.method == 'POST':
        form = CarrierCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            Carrier.objects.create(user=user, name=form.cleaned_data['name'], phone_number=form.cleaned_data['phone_number'], email=form.cleaned_data['email'])
            return render(request, "registration/register_complete.html")
        return render(request, 'registration/carrier_register.html',{'form':form})
    else:
        form = CarrierCreateForm()
        return render(request, 'registration/carrier_register.html',{'form':form})

@login_required
def browse(request):
    if request.method == 'GET':
        user = User.objects.get(username = request.user.username)
        cart = []
        total = 0.00
        if user.buyer.current_order != None:
            current_order = user.buyer.current_order
            itemsInCart = current_order.cartlist
            # quants = Quantities.objects.get(order=current_order)

            
            for it in itemsInCart:
                q = Quantities.objects.get(order=current_order,foodItem=it)
                if q.quantity > 0:
                    cart.append({'name':it.name, 'price':it.price, 'quantity':q.quantity, 'id':it.id})
                    total = total + (it.price * q.quantity)
        if cart != []:
            restaurants = [itemsInCart[0].restaurant]
        else:
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
        q = Quantities.objects.filter(order=order,foodItem=item).first()
        if q != None:
            q.quantity = q.quantity + 1
            q.save()
        else:
            q = Quantities.objects.create(order=order,foodItem=item,quantity=1)
            q.save()
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
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        buyer = request.user.buyer
        if form.is_valid():
            if form.cleaned_data['name'] != "":
                buyer.name = form.cleaned_data['name']
            if form.cleaned_data['address'] != "":
                buyer.address = form.cleaned_data['address']
            if form.cleaned_data['phone_number'] != "":
                buyer.phone_number = form.cleaned_data['phone_number']
            if form.cleaned_data['credit_card_number'] != "":
                buyer.credit_card_number = form.cleaned_data['credit_card_number']
            if form.cleaned_data['credit_card_exp'] != "":
                buyer.credit_card_exp = form.cleaned_data['credit_card_exp']
            if form.cleaned_data['credit_card_sec'] != "":
                buyer.credit_card_sec = form.cleaned_data['credit_card_sec']
            buyer.save()
            #Process
            return render(request, "profile.html", {"form":form, "success":True})
        else: 
            return render(request, "profile.html", {"form":form, "error":True})
    else:
        form = ProfileForm()
        buyer = request.user.buyer
        ccn = "**** **** **** " + buyer.credit_card_number[12:17] if buyer.credit_card_number else "-"
        cce = buyer.credit_card_exp if buyer.credit_card_exp else "-"
        ccs = "***" if buyer.credit_card_sec else ""
        defaults = {"name":buyer.name,"address":buyer.address,"phone_number":buyer.phone_number,"credit_card_number":ccn, "credit_card_expiration" : cce, "credit_card_security":ccs}
        return render(request, "profile.html", {"form":form, "defaults":defaults})
        # form.name = buyer.name
    # b = request.user.buyer
    # buyer = {'Username': request.user.username, 'Full Name': b.name, 'address' : b.address, 'phone_number' : b.phone_number, 'credit_card' : '1234'}

    

@login_required
def checkout(request):
    pass #checkout 
