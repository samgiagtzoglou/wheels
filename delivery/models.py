from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    def __str__(self):
        return self.name

class Carrier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activatedCarrier = models.BooleanField(default=False)
    # credit_card_number = models.CharField(max_length=16, blank=True,null=True)
    # credit_card_exp = models.CharField(max_length=5, blank=True,null=True)
    # credit_card_sec = models.CharField(max_length=4, blank=True,null=True)

    # orders = models.ManyToManyField(Order)
    def __str__(self):
        return self.name if self.name is not None else self.user.username

class Order(models.Model):
    user = models.ForeignKey(User)
    cart = models.ManyToManyField(FoodItem, through="Quantities")
    status = models.CharField(max_length=30, default="Incomplete")
    carrier = models.ForeignKey(Carrier, blank=True,null=True)

    @property
    def cartlist(self):
        return list(self.cart.all())

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True,null=True)
    email = models.CharField(max_length=40, blank=True,null=True)
    address = models.CharField(max_length=50, blank=True,null=True)
    phone_number = models.CharField(max_length=20, blank=True,null=True)
    credit_card_number = models.CharField(max_length=16, blank=True,null=True)
    credit_card_exp = models.CharField(max_length=5, blank=True,null=True)
    credit_card_sec = models.CharField(max_length=4, blank=True,null=True)

    current_order = models.ForeignKey(Order,blank=True,null=True)
    
    def __str__(self):
        return self.name if self.name is not None else self.user.username

class Quantities(models.Model):
    order = models.ForeignKey(Order)
    foodItem = models.ForeignKey(FoodItem)
    quantity = models.IntegerField()