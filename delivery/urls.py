from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register', views.register, name='register'),
    url(r'^browse', views.browse, name='browse'),
    url(r'^checkout', views.checkout, name='checkout'),
    url('^', include('django.contrib.auth.urls'))
]
