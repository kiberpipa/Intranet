import datetime
import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from intranet.org.models import Event
from intranet.feedjack.models import Post
from intranet.photologue.models import Photo
from intranet.www.models import Ticker, News

def index(request):
    return render_to_response('www/index.html', {
        'events': Event.objects.filter(start_date__gte=datetime.datetime.today()).order_by('start_date')[0:8],
        'planet': Post.objects.all().order_by('date_modified')[0:2],
        'gallery': Photo.objects.all().order_by('date_added')[0:2],
        'news': Ticker.objects.filter(is_active=True),
        },
        context_instance=RequestContext(request))


def event(request, slug):
    return render_to_response('www/event.html', {
        'event': Event.objects.get(slug=slug),
        }, 
        context_instance=RequestContext(request))

def news(request, slug):
    return render_to_response('www/news.html', {
        'news': News.objects.get(slug=slug),
        },
        context_instance=RequestContext(request))

def compat(request):
    if request.GET.has_key('sid'):
        return HttpResponseRedirect('/news/' + News.objects.get(id=request.GET['sid']).slug)
    else:
        return HttpResponseRedirect('/')
