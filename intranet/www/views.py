import datetime
import re
from StringIO import StringIO

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.conf import settings
from django.core.mail import send_mail

from intranet.org.models import Event
from intranet.feedjack.models import Post
from intranet.photologue.models import Photo, Gallery
from intranet.www.models import Ticker, News

def gallery(request, id):
    ret = ''
    for g in Gallery.objects.get(pk=id).photos.all():
        #<li><img src="img/flowing-rock.jpg" alt="Flowing Rock" title="Flowing Rock Caption"></li>
        ret += '<li><img src="%s"></li>\n' % (g.get_normal_url())

    return HttpResponse(ret)

def index(request):
    # FIXME: next line throws an error on empty db
    next = Event.objects.filter(public=True, start_date__gte=datetime.datetime.today()).order_by('start_date')[0]
    #forcing the evalutation of query set :-/. anyone got better ideas?
    events = list(Event.objects.filter(public=True).order_by('start_date'))
    position = events.index(next)
    jsevents = ''
    for e in events[position-100:]:
        tmp= re.sub('"', '\\"', e.__unicode__())
        jsevents += '"<img width=\\"274\\" height=\\"200\\" src=\\"%swww/images/img-upcoming.gif\\" alt=\\"slika\\" /><div class=\\"present-event-text\\">%s</div>",' % (settings.MEDIA_URL, tmp)
    jsevents = re.sub(',$', '', jsevents)
        
    return render_to_response('www/index.html', {
        'events': events[position:position+8],
        'jsevents': jsevents,
        'gallery': Photo.objects.all().order_by('date_added')[0:2],
        'ticker': Ticker.objects.filter(is_active=True),
        'news': News.objects.order_by('-date')[0:4],
        'planet': Post.objects.order_by('-date_modified')[:4],
    }, context_instance=RequestContext(request))

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
        return HttpResponsePermanentRedirect(News.objects.get(id=request.GET['sid']).get_absolute_url())
    if request.GET.has_key('eid'):
        #calendar crap
        return HttpResponsePermanentRedirect(News.objects.get(calendar_id=request.GET['eid']).get_absolute_url())
    if request.GET.has_key('ceid'):
        ceid = request.GET['ceid']
        if ceid == 11:
            return HttpResponsePermanentRedirect('/community/')
        else:
            return HttpResponsePermanentRedirect('/about/')

#    elif request.GET.has_key('set_albumName')
#        #`gallery crap'
#        if request.GET.has_key('id'):
#            #image has been requested
#           pass 
#        else:
#            #album has been requested
#            pass
#
    #we have a problem
    send_mail('b00, wh00, 404', 'PATH_INFO: %s\nQUERY_STRING: %s' % (request.META['PATH_INFO'], request.META['QUERY_STRING']), 'intranet@kiberpipa.org', [a[1] for a in settings.ADMINS], fail_silently=True)
    return HttpResponsePermanentRedirect('/')

def calendar(request):
    day = datetime.timedelta(1)
    today = datetime.date.today()

    begin= datetime.date(today.year, today.month, 1)

    #find the begening of the week in which this month starts
    while begin.weekday() != 0:
        begin = begin - day

    dates = []
    #loop till the end of the week in which this months ends
    while not ( begin.month == today.month + 1 and begin.weekday() == 0):
        dates += [(begin, Event.objects.filter(start_date__year = begin.year, start_date__month = begin.month, start_date__day = begin.day))]
        begin = begin + day


    return render_to_response('www/calendar.html', {
        'dates': dates,
        },
        context_instance=RequestContext(request))

def utcize(date):
    from pytz import timezone, utc
    lj = timezone('Europe/Ljubljana')
    tmp = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, tzinfo=lj)
    return tmp.astimezone(utc) #rfc wants utc here


def ical(request, month=None):
    from django.utils.encoding import *
    encoding = 'latin2'
    cal = ['BEGIN:VCALENDAR', 
        'SUMMARY:%s -- Dogodki v Kiberpipi' % datetime.datetime.today().strftime('%B'), 
        'PRODID: -//Kiberpipa//NONSGML intranet//EN', 
        'VERSION:2.0', '']
    if month:
        events = Event.objects.filter(public=True, start_date__year=datetime.datetime.today().year, start_date__month=datetime.datetime.today().month).order_by('chg_date')
        response = HttpResponse(mimetype='application/octet-stream')
        response['Content-Disposition'] = "attachment; filename=" + datetime.datetime.today().strftime('%B') + '.vcs'
    else: 
        events = Event.objects.order_by('start_date')
        response = HttpResponse()

    for e in events:
        #ther's gotta be a nicer way to do this
        end_date = e.start_date + datetime.timedelta(hours=e.length.hour,  minutes=e.length.minute)
        last_mod = utcize(e.chg_date)
        pub_date = utcize(e.pub_date)

        cal.extend((
            'BEGIN:VEVENT',
            'ORGANIZER;CN=Kiberpipa:MAILTO:info@kiberpipa.org',
            pub_date.strftime('DTSTAMP:%Y%m%dT%H%M%SZ'),
            pub_date.strftime('CREATED:%Y%m%dT%H%M%SZ'),
            e.start_date.strftime('DTSTART:%Y%m%dT%H%M%S'),
            e.start_date.strftime('UID:events@kiberpipa.org-%Y%m%dT%H%M%S'),
            end_date.strftime('DTEND:%Y%m%dT%H%M%S'),
            last_mod.strftime('LAST-MODIFIED:%Y%m%dT%H%M%SZ'),
            'SUMMARY:%s' % e.title,
            'TRANSP:OPAQUE',
            'END:VEVENT',
            ''))

    cal.append('END:VCALENDAR')
    ret = "\r\n".join(cal)
    ret = smart_unicode("\r\n".join(cal), encoding=encoding, strings_only=False, errors='strict')
    response.write(ret)
    return response

