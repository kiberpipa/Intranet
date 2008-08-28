from django.shortcuts import render_to_response
from intranet.org.models import Event
from django.template import RequestContext

from intranet.feedjack.models import Post
from intranet.photologue.models import Photo

def index(request):
    last9 = Event.objects.all().order_by('-start_date')[0:8] 
    return render_to_response('www/index.html', {
        'last3': last9[0:3], 
        'pre6': last9[3:],
        'planet': Post.objects.all().order_by('date_modified')[0:2],
        'gallery': Photo.objects.all().order_by('date_added')[0:2],
        },
        context_instance=RequestContext(request))
