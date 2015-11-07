from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

def home(request):
    return render(request, 'index.html')

def user_logout(request):
    logout(request)