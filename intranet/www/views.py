# *-* coding: utf-8 *-*

import datetime
import time
from calendar import Calendar

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.http import HttpResponsePermanentRedirect, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.comments.views.comments import post_comment
from django.views.generic.list_detail import object_list
from django.utils.translation import ugettext as _
from feedjack.models import Post
from honeypot.decorators import check_honeypot
from dateutil.relativedelta import relativedelta

from intranet.org.models import to_utc, Event, Email, EmailBlacklist
from intranet.org.forms import EmailBlacklistForm
from intranet.www.models import Ticker, News
from intranet.www.forms import EmailForm, EventContactForm
from pipa.video.models import Video


def anti_spam(request):
    # make sure users have taken at least 5 seconds to read
    # this page before writing a comment (spam bots don't)
    # TODO: replace this with honeypot method
    if int(request.POST['timestamp']) + 5 > int(datetime.datetime.now().strftime('%s')):
        return HttpResponsePermanentRedirect('/')
    return post_comment(request)


def index(request):

    return render_to_response('www/index.html', {
        'events': Event.objects.filter(public=True, start_date__gte=datetime.datetime.today()).order_by('start_date'),
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
        position = events.index(next) - 1
    except IndexError:
        events = Event.objects.filter(public=True, start_date__gte=month).order_by('start_date')
        position = events.count() - 1

    return render_to_response('www/ajax_index_events.html', {
      'position': position,
      'events': events,
    }, context_instance=RequestContext(request))


def ajax_add_mail(request, event, email):
    event = get_object_or_404(Event, pk=event)
    form = EmailForm({'email': email})
    if form.is_valid():
        email = Email.objects.get_or_create(email=form.cleaned_data['email'])[0]
        if email in event.emails.all():
            message = _(u'You have already subscribed to this event.')
        else:
            event.emails.add(email)
            event.save()
            message = _(u'We will send you a notification when the video will be available.')
    else:
        message = _(u'Please enter a valid email address')

    return HttpResponse(message)


def event(request, slug, id):
    event = get_object_or_404(Event, pk=id)
    if not request.path.endswith(event.get_public_url()):
        return HttpResponseRedirect(event.get_public_url())
    return render_to_response('www/event.html', {
        'event': event,
        'form': EmailForm(),
        },
        context_instance=RequestContext(request))


def news_detail(request, slug=None, id=None):
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


def calendar(request, year=None, month=None, en=False):
    today = datetime.date.today()
    year = int(year or today.year)
    month = int(month or today.month)
    now = datetime.date(year, month, 15)
    cal = Calendar().monthdatescalendar(year, month)
    events = []

    for week in cal:
        for day in week:
            events.append([day, Event.objects.filter(start_date__year=day.year, start_date__month=day.month, start_date__day=day.day)])

    next_month = events[15][0] + relativedelta(months=+1)
    prev_month = events[15][0] + relativedelta(months=-1)

    return render_to_response('www/calendar.html', {
        'dates': events,
        'prev': reverse('intranet.www.views.calendar', kwargs=dict(year=prev_month.year, month=prev_month.month)),
        'next': reverse('intranet.www.views.calendar', kwargs=dict(year=next_month.year, month=next_month.month)),
        'now': now,
        },
        context_instance=RequestContext(request))


def ical(request):
    cal = [u'BEGIN:VCALENDAR',
        u'PRODID: -//Kiberpipa//NONSGML intranet//EN',
        u'VERSION:2.0']
    # DO NOT uncomment. Kulturnik.si parser breaks.
    #cal.append('SUMMARY:Dogodki v Kiberpipi')
    events = Event.objects.order_by('-chg_date')[:20]
    response = HttpResponse(mimetype='text/calendar; charset=UTF-8')
    cal.append(u'')

    for e in events:
        # there's gotta be a nicer way to do this
        # TODO: yes, use icalendar library
        # http://pypi.python.org/pypi/icalendar/
        if e.public:
            classification = u'PUBLIC'
        else:
            continue
            #classification = u'PRIVATE'

        cal.extend((
            u'BEGIN:VEVENT',
            # DO NOT uncomment. Kulturnik.si parser breaks.
            #'METHOD:REQUEST',
            u'SEQUENCE:%s' % e.sequence,
            u'ORGANIZER;CN=Kiberpipa:MAILTO:info@kiberpipa.org',
            time.strftime(u'DTSTAMP:%Y%m%dT%H%M%SZ', to_utc(e.start_date)),
            #pub_date.strftime('CREATED:%Y%m%dT%H%M%SZ'),
            time.strftime(u'DTSTART:%Y%m%dT%H%M%S', to_utc(e.start_date)),
            u'UID:event-%s@kiberpipa.org' % e.id,
            time.strftime(u'DTEND:%Y%m%dT%H%M%S', to_utc(e.end_date)),
            time.strftime(u'LAST-MODIFIED:%Y%m%dT%H%M%SZ', to_utc(e.chg_date)),
            u'SUMMARY:%s: %s' % (unicode(e.project), e.title),
            u'URL:http://www.kiberpipa.org%s' % e.get_public_url(),
            u'CLASS:%s' % classification,
            u'LOCATION:Kiberpipa, %s' % e.place,
            u'CATEGORIES:%s' % ','.join([e.project.name, e.category.name]),
            u'TRANSP:OPAQUE',
            u'END:VEVENT',
            u''))

    cal.append(u'END:VCALENDAR')
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
    return object_list(request, queryset=queryset[:10], template_name='www/news_list.html')


def odjava(request):
    message = ''
    success = False
    if request.method == 'POST':
        form = EmailBlacklistForm(request.POST)
        if form.is_valid():
            message = _(u'Your email address has been removed from our messaging list.')
            form.save()
            success = True
        else:
            try:
                EmailBlacklist.objects.get(blacklisted=request.POST['blacklisted'].strip())
                message = _(u'Your email address has been removed from our messaging list.')
                success = True
            except EmailBlacklist.DoesNotExist:
                pass
    else:
        form = EmailBlacklistForm(initial={'blacklisted': request.GET.get('email', None)})

    context = {
        'form': form,
        'message': message,
        'success': success,
        }
    return render_to_response('www/odjava.html', RequestContext(request, context))


@check_honeypot
def facilities(request):
    """Facilities info and contact form"""
    if request.method == 'POST':
        form = EventContactForm(request.POST)
        if form.is_valid():
            text = get_template('mail/facilities_request.txt').render(Context(form.cleaned_data))
            send_mail("Povpraševanje o prostorih", text, settings.DEFAULT_FROM_EMAIL, ['info@kiberpipa.org'])
            done = _(u'Your rental inquiry has been sent. We will answer it in a couple of work days')
    else:
        form = EventContactForm()
    return render_to_response('www/facilities.html', RequestContext(request, locals()))
