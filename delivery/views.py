from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import CarrierCreateForm, BuyerCreateForm, ProfileForm
from models import Buyer, Carrier, Restaurant, Order, FoodItem, Quantities
from django.shortcuts import redirect

def home(request):
    return views.login(request)

# def login(request):
#     x = views.login(request)
#     print x
#     # user = User.objects.get(username = request.user.username)
#     if user.buyer:
#         return "Carrier logged in"
#     return x

def register(request):
    if request.method == 'POST':
        form = BuyerCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            Buyer.objects.create(user=user, current_order=None, email=form.cleaned_data['email'])
            Carrier.objects.create(user=user)
            return render(request, "registration/register_complete.html")
        return "Error"
    else:
        form = BuyerCreateForm()

        return render(request, 'registration/register.html',{'form':form})

@login_required
def register_carrier(request):
    if request.method == 'POST':
        form = CarrierCreateForm(request.POST)
        if form.is_valid() and form.cleaned_data['agreed']==True:
            request.user.carrier.activatedCarrier = True
            request.user.carrier.save()
            return render(request, "registration/register_complete.html")
        return render(request, 'registration/carrier_register.html',{'form':form})
    else:
        form = CarrierCreateForm()
        return render(request, 'registration/carrier_register.html',{'form':form})

@login_required
def handle(request):
    if request.method == 'GET':
        if request.user.carrier.activatedCarrier:
            return redirect('dashboard')
        else:
            return redirect('browse')
    return 'lol'

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
def dashboard(request):
    user = request.user
    carrier = request.user.carrier
    current_orders = []
    open_orders = []
    for o in Order.objects.filter(status="Pending"):
        cart = []
        total = 0.0
        for it in o.cartlist:
            q = Quantities.objects.get(order=o,foodItem=it)
            if q.quantity > 0:
                cart.append({'name':it.name, 'price':it.price, 'quantity':q.quantity, 'id':it.id})
                total = total + (it.price * q.quantity)
        open_orders.append({'cart':cart, 'total':total, 'buyer': o.user.buyer, 'restaurant' : o.cartlist[0].restaurant, 'id':o.id})
    for c in Order.objects.filter(carrier=carrier, status__in=["Claimed","Picked Up","Delivered"]):
        cart = []
        total = 0.0
        for it in c.cartlist:
            q = Quantities.objects.get(order=c,foodItem=it)
            if q.quantity > 0:
                cart.append({'name':it.name, 'price':it.price, 'quantity':q.quantity, 'id':it.id})
                total = total + (it.price * q.quantity)
        current_orders.append({'cart':cart, 'total':total, 'buyer': c.user.buyer, 'restaurant' : c.cartlist[0].restaurant, 'id':c.id, 'status':c.status})
    return render(request, 'dashboard.html', {"user":user, 'current_orders':current_orders, 'open_orders':open_orders})

@login_required
def claimOrder(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status=="Pending":
        order.carrier = request.user.carrier
        order.status = "Claimed"
        order.save()
    return redirect('dashboard')

@login_required
def markPickedUp(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status=="Claimed":
        order.carrier = request.user.carrier
        order.status = "Picked Up"
        order.save()
    return redirect('dashboard')

@login_required
def markDelivered(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status=="Picked Up":
        order.carrier = request.user.carrier
        order.status = "Delivered"
        order.save()
    return redirect('dashboard')

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
    buyer = request.user.buyer
    order = request.user.buyer.current_order
    cart = []
    itemsInCart = order.cartlist
    total = 0.0
    for it in itemsInCart:
        q = Quantities.objects.get(order=order,foodItem=it)
        if q.quantity > 0:
            cart.append({'name':it.name, 'price':it.price, 'quantity':q.quantity, 'id':it.id})
            total = total + (it.price * q.quantity)

    restaurant = itemsInCart[0].restaurant
    return render(request, "checkout.html", {'order' : order, 'itemsInCart':cart})

@login_required
def confirm(request):
    buyer = request.user.buyer
    order = request.user.buyer.current_order
    if order.status == "Incomplete":
        order.status = "Pending"
        order.save()
    cart = []
    itemsInCart = order.cartlist
    total = 0.0
    for it in itemsInCart:
        q = Quantities.objects.get(order=order,foodItem=it)
        if q.quantity > 0:
            cart.append({'name':it.name, 'price':it.price, 'quantity':q.quantity, 'id':it.id})
            total = total + (it.price * q.quantity)

    restaurant = itemsInCart[0].restaurant
    return render(request, "confirm.html", {'order' : order, 'itemsInCart':cart})
