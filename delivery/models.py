from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=30)

class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=30)
    price = models.FloatField()


class Order(models.Model):
    user = models.ForeignKey(User)
    cart = models.ManyToManyField(FoodItem)

    @property
    def cartlist(self):
        return list(self.cart.all())

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_order = models.ForeignKey(Order,blank=True,null=True)
    
# Create your models here.
