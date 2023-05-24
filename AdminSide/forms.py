from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		# fields = '__all___'
		fields = ['first_name','last_name','username','email','password1','password2']


class UpdateUser(UserChangeForm):
	update_password = forms.BooleanField(required=False)
	new_password1 = forms.CharField(label='New Password',max_length=128,widget=forms.PasswordInput,required=False)
	new_password2 = forms.CharField(label='Confirm New Password',max_length=128,widget=forms.PasswordInput,required=False)

	# new_password1 = forms.CharField(label='New password', max_length=128, widget=forms.PasswordInput, required=False)
    # new_password2 = forms.CharField(label='Confirm new password', max_length=128, widget=forms.PasswordInput, required=False)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','new_password1','new_password2']
