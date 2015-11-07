from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, views

def home(request):
    
    return views.login(request)

def user_logout(request):
    logout(request)