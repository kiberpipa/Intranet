import datetime
import re
from StringIO import StringIO

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core import serializers
from django.core.urlresolvers import reverse

from intranet.org.models import Event
from intranet.feedjack.models import Post
from intranet.photologue.models import Photo, Gallery
from intranet.www.models import Ticker, News, Video
import simplejson

def gallery(request, id):
    try:
        gallery = Gallery.objects.get(title=id)
    except Gallery.DoesNotExist:
        gallery = Gallery.objects.get(pk=id)
    ret = ''
    i = 0

    #return HttpResponse(serializers.serialize("json", [x.get_normal_url() for x in gallery.photos.all()]))
    #return HttpResponse([x.get_normal_url() for x in gallery.photos.all()])
    
    nice_pictures = list()
    for p in gallery.photos.all():
        nice_pictures.append({'normal_url':p.get_normal_url(),
                                'full_url':p.image.url,
                                'exif':p.EXIF})
    return HttpResponse(simplejson.dumps(nice_pictures))
    #for g in gallery.photos.all():
    #    i += 1
    #    ret += '<li'
    #    if i == 1:
    #        ret += ' id="active"'
    #    ret += '><img src="%s" class="img%s"></li>\n' % (g.get_normal_url(), g.id)

        #ret += '<div id="%s" style="display: none"><div id="exif">b00 wh00 %s</div></div>' % (g.get_normal_url(), g.title)
    #    ret += '<div id="img%s" style="display: none">b00 wh00 %s</div>' % (g.id, g.title)

    return HttpResponse(ret)

def index(request):
    # FIXME: next line throws an error on empty db
    next = Event.objects.filter(public=True, start_date__gte=datetime.datetime.today()).order_by('start_date')[0]
    month = datetime.datetime.today() - datetime.timedelta(30)
    #forcing the evalutation of query set :-/. anyone got better ideas?
    events = list(Event.objects.filter(public=True, start_date__gte=month).order_by('start_date'))
    position = events.index(next) - 2

    return render_to_response('www/index.html', {
        'position': position,
        'events': events,
        'gallery': Photo.objects.all().order_by('date_added')[0:2],
        'ticker': Ticker.objects.filter(is_active=True),
        'news': News.objects.order_by('-date')[0:4],
        'planet': Post.objects.order_by('-date_modified')[:4],
        'videos': Video.objects.order_by('-pub_date')[:4],
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

def calendar(request, year=None, month=None, en=False):
    day = datetime.timedelta(1)
    today = datetime.date.today()
    if month:
        today = datetime.date(int(year), int(month), 1)

    begin = datetime.date(today.year, today.month, 1)

    #find the begening of the week in which this month starts
    while begin.weekday() != 0:
        begin = begin - day

    dates = []
    #loop till the end of the week in which this months ends
    if today.month == 12:
        next_month = 1
        next_year = today.year + 1
        prev_month = today.month - 1
        prev_year = today.year
    elif today.month == 1:
        next_month = today.month + 1
        next_year = today.year
        prev_month = 12
        prev_year = today.year - 1
    else:
        next_month = today.month + 1
        next_year = today.year
        prev_year = today.year
        prev_month = today.month - 1
    while not ( begin.month == next_month and begin.weekday() == 0):
        dates += [(begin, Event.objects.filter(start_date__year = begin.year, start_date__month = begin.month, start_date__day = begin.day))]
        begin = begin + day


    if en:
        template='www/calendar-en.html'
    else:
        template='www/calendar.html'

    return render_to_response(template, {
        'dates': dates,
        'prev': reverse('intranet.www.views.calendar', args=['%s/%s' % (prev_year, prev_month)]),
        'next': reverse('intranet.www.views.calendar', args=['%s/%s' % (next_year, next_month)]),
        },
        context_instance=RequestContext(request))

def utcize(date):
    from pytz import timezone, utc
    lj = timezone('Europe/Ljubljana')
    tmp = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, tzinfo=lj)
    return tmp.astimezone(utc) #rfc wants utc here


def ical(request, month=None):
    cal = ['BEGIN:VCALENDAR', 
        'PRODID: -//Kiberpipa//NONSGML intranet//EN', 
        'VERSION:2.0']
    if month:
        cal.append('SUMMARY:%s -- Dogodki v Kiberpipi' % datetime.datetime.today().strftime('%B'))
        events = Event.objects.filter(public=True, start_date__year=datetime.datetime.today().year, start_date__month=datetime.datetime.today().month).order_by('chg_date')[:20]
        response = HttpResponse(mimetype='application/octet-stream')
        response['Content-Disposition'] = "attachment; filename=" + datetime.datetime.today().strftime('%B') + '.vcs'
    else: 
        cal.append('SUMMARY:Dogodki v Kiberpipi')
        events = Event.objects.order_by('-chg_date')[:20]
        response = HttpResponse(mimetype='text/calendar')
    cal.append('')

    for e in events:
        #ther's gotta be a nicer way to do this
        end_date = e.start_date + datetime.timedelta(hours=e.length.hour,  minutes=e.length.minute)
        last_mod = utcize(e.chg_date)
        pub_date = utcize(e.pub_date)

        cal.extend((
            'BEGIN:VEVENT',
            'METHOD:REQUEST',
            'SEQUENCE:%s' % e.sequence,
            'ORGANIZER;CN=Kiberpipa:MAILTO:info@kiberpipa.org',
            e.start_date.strftime('DTSTAMP:%Y%m%dT%H%M%SZ'),
            #pub_date.strftime('CREATED:%Y%m%dT%H%M%SZ'),
            e.start_date.strftime('DTSTART:%Y%m%dT%H%M%S'),
            'UID:event-%s@kiberpipa.org' % e.id,
            end_date.strftime('DTEND:%Y%m%dT%H%M%S'),
            last_mod.strftime('LAST-MODIFIED:%Y%m%dT%H%M%SZ'),
            'SUMMARY:%s: %s' % (e.project, e.title),
            'DESCRIPTION:%s' % e.get_public_url(),
            'TRANSP:OPAQUE',
            'END:VEVENT',
            ''))

    cal.append('END:VCALENDAR')
    ret = u'\r\n'.join(cal)
    response.write(ret)
    return response


def rss(request):
	return render_to_response('www/rss.html', context_instance=RequestContext(request))
