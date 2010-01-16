
from django import forms

class LDAPPasswordChangeForm(forms.Form):
	old_password = forms.CharField(max_length='200', widget=forms.PasswordInput)
	new_password = forms.CharField(max_length='200', widget=forms.PasswordInput)
	new_password_confirm = forms.CharField(max_length='200', widget=forms.PasswordInput)

