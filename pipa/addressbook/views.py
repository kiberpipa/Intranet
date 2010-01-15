
from pipa.addressbook.models import PipaProfile
from django.shortcuts import render_to_response
from django.template import RequestContext

def alumni(request):
	profiles = PipaProfile.objects.filter(show_profile=True).order_by('user__first_name')
	context = { 'profiles': profiles }
	return render_to_response("alumni/alumni.html", RequestContext(request, context))

