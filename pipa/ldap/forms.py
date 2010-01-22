from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LDAPPasswordChangeForm(forms.Form):
	old_password = forms.CharField(max_length='200', widget=forms.PasswordInput)
	new_password = forms.CharField(max_length='200', widget=forms.PasswordInput)
	new_password_confirm = forms.CharField(max_length='200', widget=forms.PasswordInput)

class LoginForm(AuthenticationForm)
    remember_me = forms.BooleanField()
