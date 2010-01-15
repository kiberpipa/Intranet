
from django.shortcuts import render_to_response
from django.template import RequestContext

from pipa.addressbook.models import PipaProfile
from pipa.addressbook.forms import ProfileForm

def alumni(request):
	profiles = PipaProfile.objects.filter(show_profile=True).order_by('user__first_name')
	context = { 'profiles': profiles }
	return render_to_response("alumni/alumni.html", RequestContext(request, context))

def addressbook(request):
	profile = request.user.get_profile()
	profile_form = ProfileForm(instance=profile, initial={'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
	
	
	context = {'profile_form': profile_form,
		'object_list': PipaProfile.objects.all(),
		}
	
	return render_to_response("org/addressbook.html", RequestContext(request, context))
