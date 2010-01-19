
from django.forms import ModelForm
from django import forms
from pipa.addressbook.models import PipaProfile
from django.contrib.admin.widgets import AdminFileWidget

class ProfileForm(ModelForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	description = forms.CharField(widget=forms.Textarea(attrs={'cols':'32','rows':'10'}))
	sshpubkey = forms.CharField(widget=forms.Textarea(attrs={'cols':'32','rows':'10'}))
	image = forms.ImageField(widget=AdminFileWidget)
	
	class Meta:
		model = PipaProfile
		exclude = ('user',)
		# don't touch, this works in 1.1
		fields = tuple(['email', 'first_name', 'last_name'] + [f.name for f in model._meta.fields if f.__class__.__name__ != 'AutoField'])
