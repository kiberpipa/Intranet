# *-* coding: utf-8 *-*

import datetime
import time
import logging
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
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from feedjack.models import Post
from dateutil.relativedelta import relativedelta
from django_mailman.models import List
from haystack.query import SearchQuerySet

from intranet.org.models import to_utc, Event, Email
from intranet.www.models import News
from intranet.www.forms import EmailForm, EventContactForm
from pipa.video.models import Video
from pipa.video.utils import is_streaming


logger = logging.getLogger(__name__)


@csrf_protect
def anti_spam(request):
    # make sure users have taken at least 5 seconds to read
    # this page before writing a comment (spam bots don't)
    # TODO: replace this with honeypot method
    if int(request.POST['timestamp']) + 5 > int(datetime.datetime.now().strftime('%s')):
        return HttpResponsePermanentRedirect('/')
    return post_comment(request)


def index(request):
    return render_to_response('www/index.html', {
        'news': News.objects.order_by('-date')[0:4],
        'planet': Post.objects.order_by('-date_modified')[:4],
        'videos': Video.objects.order_by('-pub_date')[:4],
        'emailform': EmailForm,
    }, context_instance=RequestContext(request))


# TODO: cache for 3min
def ajax_index_events(request):
    past_month = datetime.datetime.today() - datetime.timedelta(30)
    last_midnight = datetime.datetime.today().replace(hour=0, minute=0, second=0)

    events = Event.objects.filter(public=True, start_date__gte=past_month).order_by('start_date')
    try:
        next = Event.objects.filter(public=True, start_date__gte=last_midnight).order_by('start_date')[0]
        position = list(events).index(next)
    except IndexError:
        # if we don't have upcoming events, show this past_month events
        position = events.count() - 1

    streaming_event = None
    if is_streaming():
        try:
            streaming_event = Event.objects.filter(public=True, start_date__lte=datetime.datetime.now()).order_by('-start_date')[0]
        except IndexError:
            pass

    return render_to_response('www/ajax_index_events.html', locals(),
        context_instance=RequestContext(request))


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


def ajax_subscribe_mailinglist(request):
    # TODO: refactor to form validation
    # TODO: django-mailman does not handle situations if member already exists
    # TODO: invite instead of subscribe (patch for django-mailman)
    form = EmailForm(request.POST or None)
    if form.is_valid():
        try:
            mailman_list = List.objects.get(id=1)
            mailman_list.subscribe(form.cleaned_data['email'])
            return HttpResponse(_(u'Sent approval email!'))
        except Exception, e:
            logger.exception('Mailing list subscription problem')
            return HttpResponse(e.message)
    else:
        return HttpResponse(_(u'Wrong email!'))


def event(request, slug=None, id=None):
    event = get_object_or_404(Event, pk=id, public=True)
    if not request.path.endswith(event.get_public_url()):
        return HttpResponseRedirect(event.get_public_url())

    mlt = SearchQuerySet().filter(is_public=True).more_like_this(event)[:5]

    return render_to_response('www/event.html', {
        'event': event,
        'form': EmailForm(),
        'related_content': mlt,
        },
        context_instance=RequestContext(request))


@csrf_protect
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
            events.append([day, Event.objects.filter(start_date__year=day.year, start_date__month=day.month, start_date__day=day.day).order_by('start_date')])

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
