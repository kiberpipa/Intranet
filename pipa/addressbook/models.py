from django.db import models
from django.contrib.auth.models import User

class PipaProfile(models.Model):
	# former is_active: if it's set, show the profile on alumni page
	show_profile = models.BooleanField(default=False)
	
	description = models.TextField(max_length=400, blank=True, null=True)
	user = models.ForeignKey(User, unique=True)
	image = models.ImageField(upload_to='alumni/', blank=True, null=True)
	
	# internal ways of contacting people, used for phonebook and such
	phone = models.CharField(max_length=150, blank=True, null=True)
	jabber = models.CharField(max_length=150, blank=True, null=True)
	msn = models.CharField(max_length=150, blank=True, null=True)
	yahoo = models.CharField(max_length=150, blank=True, null=True)
	skype = models.CharField(max_length=150, blank=True, null=True)
	
	# public profile
	blog = models.CharField(max_length=150, blank=True, null=True)
	www = models.CharField(max_length=150, blank=True, null=True)
	www_public = models.BooleanField(default=False)
	facebook = models.CharField(max_length=150, blank=True, null=True)
	facebook_public = models.BooleanField('FB public', default=False)
	twitter = models.CharField(max_length=150, blank=True, null=True)
	twitter_public = models.BooleanField(default=False)
	linkedin = models.CharField(max_length=150, blank=True, null=True)
	linkedin_public = models.BooleanField(default=False)
	flickr = models.CharField(max_length=150, blank=True, null=True)
	flickr_public = models.BooleanField(default=False)
	sshpubkey = models.TextField(max_length=4000, blank=True, null=True)
	sshpubkey_public = models.BooleanField('Key public', default=False)
	
	class Meta:
		ordering = ('user__first_name',)
	
	def __unicode__(self):
		if self.user:
			return unicode(self.user)
		else:
			return self.description

