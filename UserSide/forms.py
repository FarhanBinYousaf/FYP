from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactUs
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field,Row,Column


class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		widgets = {
        'username':forms.TextInput(attrs={'id':'nameid','placeholder':'Username'}),
        'email':forms.EmailInput(attrs={'id':'emailid','placeholder':'Email'}),
        'password':forms.PasswordInput(attrs={'id':'passwordid','placeholder':'Password'}),
        }
		



	

    