from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, views
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return views.login(request)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, "registration/register_complete.html")
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html',{'form':form})
        
def user_logout(request):
    logout(request)