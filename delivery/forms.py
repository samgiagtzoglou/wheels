from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import Buyer

class ProfileForm(forms.Form):
    name = forms.CharField(label='Full name',max_length=100)
    address = forms.CharField(label='Address',max_length=100)
    phone_number = forms.CharField(label='Phone Number',max_length=100)
    credit_card_number = forms.CharField(label='Credit Card Number',max_length=16)
    credit_card_exp = forms.CharField(label='Credit Card Exp',max_length=5)
    credit_card_sec = forms.CharField(label='Credit Card Security',max_length=4)

