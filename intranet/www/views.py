import datetime
import re
from StringIO import StringIO

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.comments.views.comments import post_comment
from django.views.generic.list_detail import object_list
from django import forms
from django.utils.translation import ugettext as _
from django.utils import simplejson

from intranet.org.models import Event, Email
from feedjack.models import Post
from intranet.www.models import Ticker, News
from pipa.video.models import Video


#if there will be any more forms we should probably create www/forms.py
class EmailForm(forms.Form):
    email = forms.EmailField()

def anti_spam(request):
    #make sure the users have taken at least 5 seconds from to read the page and write the comment (spam bots don't) 
    if int(request.POST['timestamp'])+5 > int(datetime.datetime.now().strftime('%s')):
        return HttpResponsePermanentRedirect('/')
    return post_comment(request)

def index(request):
    dogodki = Event.objects.filter(public=True, start_date__gte=datetime.datetime.today()).order_by('start_date')
    try:
        events = [dogodki[0]]
    except IndexError, e:
        events = [None]
    try:
        events.append(dogodki[1])
    except IndexError, e:
        pass

    try:
        pretekli = Event.objects.filter(public=True, start_date__lt=datetime.datetime.today()).order_by('-start_date')[0]
        events.insert(0, pretekli)
    except IndexError, e:
        events.insert(0, None)

    return render_to_response('www/index.html', {
        'events': events,
        'ticker': Ticker.objects.filter(is_active=True),
        'news': News.objects.order_by('-date')[0:4],
        'planet': Post.objects.order_by('-date_created')[:4],
        'videos': Video.objects.order_by('-pub_date')[:4],
    }, context_instance=RequestContext(request))

def ajax_index_events(request):
    month = datetime.datetime.today() - datetime.timedelta(30)
    try:
        next = Event.objects.filter(public=True, start_date__gte=datetime.datetime.today()).order_by('start_date')[0]
        #forcing the evalutation of query set :-/. anyone got better ideas?
        events = list(Event.objects.filter(public=True, start_date__gte=month).order_by('start_date'))
        position = events.index(next) -1
    except IndexError:
        events = Event.objects.filter(public=True, start_date__gte=month).order_by('start_date')
        position = events.count() -1
    
    return render_to_response('www/ajax_index_events.html', {
      'position': position,
      'events': events,  
    }, context_instance=RequestContext(request))

def ajax_add_mail(request, event, email):
    event = get_object_or_404(Event, pk=event)
    form = EmailForm({'email': email})
    if form.is_valid():
        email = Email.objects.get_or_create(email = form.cleaned_data['email'])[0]
        if email in event.emails.all():
            message = _('You are already subscribed to this event.')
        else:
            event.emails.add(email)
            event.save()
            message = _('You will recieve the notification when the video is available.')
    else:
        message = _('Please enter valid email address')
        
    return HttpResponse(message)

def event(request, date, id, slug):
    event = get_object_or_404(Event, pk=id)
    if not request.path.endswith(event.get_public_url()):
        return HttpResponseRedirect(event.get_public_url())
    return render_to_response('www/event.html', {
        'event': event,
        'form': EmailForm(),
        },
        context_instance=RequestContext(request))

def news_detail(request, slug, id=None):
    if id is None:
        n = News.objects.get(slug=slug)
        return HttpResponseRedirect(n.get_absolute_url())

    n = News.objects.get(pk=id)
    if not request.path.endswith(n.get_absolute_url()):
        return HttpResponseRedirect(n.get_absolute_url())

    return render_to_response('www/news.html', {
        'news': n,
        },
        context_instance=RequestContext(request))

def compat(request, file):
    if request.GET.has_key('sid') and re.match('^[0-9]+$', request.GET['sid']):
        #`normal news links'
        return HttpResponsePermanentRedirect(News.objects.get(id=request.GET['sid']).get_absolute_url())
    if request.GET.has_key('eid'):
        #calendar article
        return HttpResponsePermanentRedirect(News.objects.get(calendar_id=request.GET['eid']).get_absolute_url())
    if request.GET.has_key('ceid'):
        #staticni linki ki so bli na levi strani
        ceid = request.GET['ceid']
        if ceid == 11:
            return HttpResponsePermanentRedirect('/community/')
        else:
            return HttpResponsePermanentRedirect('/about/')

    if request.GET.has_key('Date'):
        #calendar listing
        date = request.GET['Date']
        return HttpResponsePermanentRedirect('/calendar/%s/%s/' % (date[:4], date[4:6]))


#    elif request.GET.has_key('set_albumName')
#        #`gallery crap'
#        if request.GET.has_key('id'):
#            #image has been requested
#           pass 
#        else:
#            #album has been requested
#            pass
#
    if request.GET.has_key('pollID') or\
        request.GET.has_key('topic') or\
        request.GET.has_key('name') and request.GET['name'] == 'Web_Links' or\
        not request.GET or\
        request.GET.has_key('name') and re.match('^http://', request.GET['name']) or\
        request.GET.has_key('module') and re.match('^http://', request.GET['module']) or\
        request.GET.has_key('op') and re.match('^http://', request.GET['op']) or\
        request.GET.has_key('op') and request.GET['op'] == 'userinfo' or\
        request.GET.has_key('name') and request.GET['name'] == 'News' or\
        request.GET.has_key('name') and request.GET['name'] == 'Comments' or\
        request.GET.has_key('name') and request.GET['name'] == 'Polls' or\
        request.GET.has_key('name') and request.GET['name'] == 'polls' or\
        request.GET.has_key('name') and request.GET['name'] == 'Your_Account' or\
        request.GET.has_key('name') and request.GET['name'] == 'Submit_News' or\
        request.GET.has_key('newlang') or\
        request.GET.has_key('op') and request.GET['op'] == 'click' or\
        request.GET.has_key('file') and request.GET['file'] == 'index' or\
        request.GET.has_key('sid') and request.GET['sid'] == '749' or\
        request.GET.has_key('sid') and request.GET['sid'] == '676' or\
        request.GET.has_key('sid') and request.GET['sid'] == '3' or\
        request.GET.has_key('module') and request.GET['module'] == 'PostCale' or\
        request.GET.has_key('module') and request.GET['module'] == 'Admin' or\
        request.GET.has_key('NAME') and request.GET['NAME'] == 'Submit_News':

        return HttpResponsePermanentRedirect('/')

    if request.GET.has_key('name') and request.GET['name'] == 'Archive' and request.GET.has_key('year') and request.GET.has_key('month'):
        return HttpResponsePermanentRedirect('/calendar/%s/%s/' % (request.GET['year'], request.GET['month']))

    if request.GET.has_key('module') and request.GET['module'] == 'RSS':
        return HttpResponsePermanentRedirect('/feeds/all/planet/')
    
    if request.GET.has_key('module') and request.GET['module'] == 'PostCalendar':
        return HttpResponsePermanentRedirect('/calendar/')

    if not (request.GET.has_key('set_albumName') or (request.GET.has_key('name') and request.GET['name'] == 'gallery')):
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

    return render_to_response('www/calendar.html', {
        'dates': dates,
        'prev': reverse('intranet.www.views.calendar', args=['%s/%s' % (prev_year, prev_month)]),
        'next': reverse('intranet.www.views.calendar', args=['%s/%s' % (next_year, next_month)]),
        'now': today,
        },
        context_instance=RequestContext(request))

def utcize(date):
    from pytz import timezone, utc
    lj = timezone('Europe/Ljubljana')
    tmp = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, tzinfo=lj)
    return tmp.astimezone(utc) #rfc wants utc here


def ical(request):
    cal = ['BEGIN:VCALENDAR', 
        'PRODID: -//Kiberpipa//NONSGML intranet//EN', 
        'VERSION:2.0']
    # DO NOT uncomment. Kulturnik.si parser breaks.
    #cal.append('SUMMARY:Dogodki v Kiberpipi')
    events = Event.objects.order_by('-chg_date')[:20]
    response = HttpResponse(mimetype='text/calendar; charset=UTF-8')
    cal.append('')

    for e in events:
        #ther's gotta be a nicer way to do this
        end_date = e.start_date + datetime.timedelta(hours=e.length.hour,  minutes=e.length.minute)
        last_mod = utcize(e.chg_date)
        pub_date = utcize(e.pub_date)

        cal.extend((
            'BEGIN:VEVENT',
            # DO NOT uncomment. Kulturnik.si parser breaks.
            #'METHOD:REQUEST',
            'SEQUENCE:%s' % e.sequence,
            'ORGANIZER;CN=Kiberpipa:MAILTO:info@kiberpipa.org',
            e.start_date.strftime('DTSTAMP:%Y%m%dT%H%M%SZ'),
            #pub_date.strftime('CREATED:%Y%m%dT%H%M%SZ'),
            e.start_date.strftime('DTSTART:%Y%m%dT%H%M%S'),
            'UID:event-%s@kiberpipa.org' % e.id,
            end_date.strftime('DTEND:%Y%m%dT%H%M%S'),
            last_mod.strftime('LAST-MODIFIED:%Y%m%dT%H%M%SZ'),
            'SUMMARY:%s: %s' % (unicode(e.project), e.title),
            'URL:%s' % e.get_public_url(),
            'LOCATION:Kiberpipa, %s' % e.place,
            'CATEGORIES:%s' % ','.join([e.project.name, e.category.name]),
            'TRANSP:OPAQUE',
            'END:VEVENT',
            ''))

    cal.append('END:VCALENDAR')
    ret = u'\r\n'.join(cal)
    response.write(ret)
    return response

def rss(request):
    return render_to_response('www/rss.html', context_instance=RequestContext(request))

# Generic views wrappers.
def press(request):
    if request.LANGUAGE_CODE == 'en':
        template = 'www/press_en.html'
    else:
        template = 'www/press.html'
    return render_to_response(template, RequestContext(request, {}))

def news_list(request):
    queryset = News.objects.order_by('-date')
    if request.LANGUAGE_CODE == 'en':
        queryset = queryset.filter(language='en')
    return object_list(request, queryset=queryset[:10], template_name= 'www/news_list.html')

