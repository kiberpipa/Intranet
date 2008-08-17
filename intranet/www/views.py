from django.shortcuts import render_to_response
from intranet.org.models import Event
# Create your views here.

def index(request):
    last9 = Event.objects.all().order_by('-start_date')[0:8] 
    #last3 = tmp[0:2]
    #pre6 = tmp[:6]
    return render_to_response('www/index.html', {
        'last3': last9[0:3], 
        'pre6': last9[3:],
        })
