from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import Buyer
from django.contrib.auth.models import User

class ProfileForm(forms.Form):
    name = forms.CharField(label='Full name',max_length=100)
    address = forms.CharField(label='Address',max_length=100)
    phone_number = forms.CharField(label='Phone Number',max_length=100)
    credit_card_number = forms.CharField(label='Credit Card Number',max_length=16)
    credit_card_exp = forms.CharField(label='Credit Card Exp',max_length=5)
    credit_card_sec = forms.CharField(label='Credit Card Security',max_length=4)

class BuyerCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(BuyerCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CarrierCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(label='Full name',max_length=100)
    phone_number = forms.CharField(label='Phone Number',max_length=100)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CarrierCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
