from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register', views.register, name='register'),
    url(r'^handle', views.handle, name='handle'),
    # url(r'^login', views.login, name='login'),
    url(r'^reg_carrier', views.register_carrier, name='reg_carrier'),
    url(r'^browse', views.browse, name='browse'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^checkout', views.checkout, name='checkout'),
    url(r'^confirm', views.confirm, name='confirm'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^addToCart/([0-9]+)', views.addItemToCart, name='addToCart'),
    url(r'^removeFromCart/([0-9]+)', views.removeItemFromCart, name='removeFromCart'),
    url(r'^claimOrder/([0-9]+)', views.claimOrder, name='claimOrder'),
    url(r'^markPickedUp/([0-9]+)', views.markPickedUp, name='markPickedUp'),
    url(r'^markDelivered/([0-9]+)', views.markDelivered, name='markDelivered'),

    url('^', include('django.contrib.auth.urls'))
]
