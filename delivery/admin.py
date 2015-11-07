from django.contrib import admin
from .models import Restaurant, FoodItem, Order

admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Order)
# Register your models here.
