
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pipa.addressbook.models import PipaProfile
from pipa.addressbook.forms import ProfileForm

def alumni(request):
	profiles = PipaProfile.objects.filter(show_profile=True).order_by('user__first_name')
	context = { 'profiles': profiles }
	return render_to_response("alumni/alumni.html", RequestContext(request, context))

@login_required
def addressbook(request):
	profile = request.user.get_profile()
	profile_form = ProfileForm(instance=profile, initial={'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
	
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
		if profile_form.is_valid():
			# this should probably be better integrated with LDAP
			request.user.email = profile_form.cleaned_data['email']
			request.user.first_name = profile_form.cleaned_data['first_name']
			request.user.last_name = profile_form.cleaned_data['last_name']
			request.user.save()
			profile_form.save()
			return HttpResponseRedirect(request.path)
	
	context = {'profile_form': profile_form,
		'object_list': PipaProfile.objects.all(),
		'user_list': User.objects.all().order_by('username'),
		}
	
	return render_to_response("org/addressbook.html", RequestContext(request, context))
