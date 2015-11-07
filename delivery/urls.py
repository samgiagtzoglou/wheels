from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register', views.register, name='register'),
    url('^', include('django.contrib.auth.urls'))

]
