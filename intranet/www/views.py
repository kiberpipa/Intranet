import datetime
import re
from StringIO import StringIO

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect, HttpResponse

from intranet.org.models import Event
from intranet.feedjack.models import Post
from intranet.photologue.models import Photo
from intranet.www.models import Ticker, News

def index(request):
    # FIXME: next line throws an error on empty db
    next = Event.objects.filter(start_date__gte=datetime.datetime.today()).order_by('start_date')[0]
    #forcing the evalutation of query set :-/. anyone got better ideas?
    events = list(Event.objects.order_by('start_date'))
    position = events.index(next)
    jsevents = ''
    for e in events[position-100:]:
        tmp= re.sub('"', '\\"', e.__unicode__())
        jsevents += '"%s",' % tmp
    jsevents = re.sub(',$', '', jsevents)
        
    return render_to_response('www/index.html', {
        'events': events[position:position+8],
        'jsevents': jsevents,
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
        #`normal news links'
        return HttpResponsePermanentRedirect('/news/' + News.objects.get(id=request.GET['sid']).slug)
#    elif request.GET.has_key('set_albumName')
#        #`gallery crap'
#        if request.GET.has_key('id'):
#            #image has been requested
#           pass 
#        else:
#            #album has been requested
#            pass
    else:
        #if we get to here we have a problem
        return HttpResponsePermanentRedirect('/')

def calendar(request):
    #construct a array of dates (from the begening of prev week for next 4 weeks)
    begin = datetime.date.today()
    day = datetime.timedelta(1)

    #find the begening of the prev week
    first = 0
    while 1:
        if begin.weekday() == 0:
            first = first  + 1

        if first == 2:
            break

        begin = begin - day
    
    #append next 4 weeks
    dates = []
    for i in range(28):
        dates += [(begin, Event.objects.filter(start_date__year = begin.year, start_date__month = begin.month, start_date__day = begin.day))]
        begin = begin + day

    return render_to_response('www/calendar.html', {
        'dates': dates,
        },
        context_instance=RequestContext(request))

def ical(request):
    cal = ['BEGIN:VCALENDAR', 'SUMMARY:%s -- Dogodki v Kiberpipi' % datetime.datetime.today().strftime('%B') ]

    for e in Event.objects.filter(start_date__month=datetime.datetime.today().month):
        cal.extend((
            'BEGIN:VEVENT',
            e.start_date.strftime('DTSTART:%Y%m%dT%H%M%S'),
            'SUMMARY:%s' % e.title,
            'END:VEVENT'))

    cal.append('END:VCALENDAR')
    response = HttpResponse(mimetype='application/octet-stream')
    response['Content-Disposition'] = "attachment; filename=" + datetime.datetime.today().strftime('%B') + '.vcs'
    response.write("\r\n".join(cal))
    return response

