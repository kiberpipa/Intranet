# *-* coding: utf-8 *-*

import datetime
import time
import logging
import urllib2
import urlparse
import json
import simplejson
from calendar import Calendar

import icalendar
import pytz
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.comments.views.comments import post_comment
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import striptags,safe,truncatewords
from feedjack.models import Post
from dateutil.relativedelta import relativedelta
from django_mailman.models import List
from haystack.query import SearchQuerySet
import twitter

from intranet.org.models import to_utc, Event, Email
from intranet.www.models import News
from intranet.www.forms import EmailForm, EventContactForm
from pipa.video.models import Video
from pipa.video.utils import is_streaming
from pipa.gallery.templatetags.photos_box import api as flickr_api


logger = logging.getLogger(__name__)
ljubljana_tz = pytz.timezone('Europe/Ljubljana')

def sort_news(x, y):
    date_x = x.date if 'date' in dir(x) else x.date_modified
    date_y = y.date if 'date' in dir(y) else y.date_modified

    return date_x < date_y

def index(request):
    # load news items (internal cms) and blog posts (members' blogs, fetched via rss)
    news = News.objects.order_by('-date')[:4]
    posts = Post.objects.order_by('-date_modified')[:4]

    # splice both of them together into one list, and sort them by date
    # but the most recent news items always comes first, even if older
    # tiny technicality - their respective models use a different date field
    both = []
    both.extend(news[1:])
    for post in posts:
        post.date = post.date_modified
        both.append(post)
    both2 = sorted(both, cmp=sort_news, reverse=True)
    both2.insert(0, news[0])

    api = twitter.Api()
    tweets = api.GetSearch(term='kiberpipa OR cyberpipe')

    try:
        pictures = []
        # http://www.flickr.com/services/api/flickr.photosets.getList.html
        json = flickr_api.flickr_call(
            method='flickr.photosets.getList',
            user_id='40437802@N07',  # http://idgettr.com/
            per_page=5,
            pages=1,
            format="json",
            nojsoncallback=1)
    except urllib2.URLError:
        pass
    else:
        r = simplejson.loads(json)
        if r.get('stat', 'error') == 'ok':
            photosets = r['photosets']['photoset']
            photosets = sorted(photosets, key=lambda x: x['date_create'], reverse=True)
            for image in photosets[:5]:
                if int(image['photos']) == 0:
                    continue
                image['thumb_url'] = settings.PHOTOS_FLICKR_SET_IMAGE_URL_N % image
                image['url'] = 'http://www.flickr.com/photos/kiberpipa/sets/%(id)s/' % image
                image['title'] = image['title']['_content']
                pictures.append(image)

    return render_to_response('www/index.html', {
        'news': news,
        'planet': posts,
        'both' : both2,
        'videos': Video.objects.order_by('-pub_date')[:4],
        'emailform': EmailForm,
        'tweets': tweets,
        'pictures': pictures,
    }, context_instance=RequestContext(request))


# TODO: cache for 3min
def ajax_index_events(request):
    now = datetime.datetime.now()
    past_month = datetime.datetime.today() - datetime.timedelta(30)
    last_midnight = datetime.datetime.today().replace(hour=0, minute=0, second=0)

    events = Event.objects.filter(public=True, start_date__gte=past_month).order_by('start_date')
    try:
        next = Event.objects.filter(public=True, start_date__gte=last_midnight).order_by('start_date')[0]
        position = list(events).index(next) - 1  # show one event before the current one
    except IndexError:
        # if we don't have upcoming events, show this past_month events
        position = events.count() - 1

    streaming_event = None
    if is_streaming():
        try:
            streaming_event = Event.objects.filter(public=True, start_date__lte=datetime.datetime.now()).order_by('-start_date')[0]
            prev = streaming_event.get_next()
            td = prev.start_date - now
            if td.days == 0 and 0 < td.seconds < 1800:
                # if there is 30min to next event, take that one
                streaming_event = prev
            # TODO: if previous event should have ended more than 3 hours ago, dont' display the stream
        except IndexError:
            pass

    # damn django resultsets aren't json-serializable.
    eventss = list()
    for event in events:
        d = dict(id=event.id, title = event.title, start_date=event.start_date)
        d['project'] = event.project.verbose_name if event.project.verbose_name else event.project.name
        d['announce'] = truncatewords(safe(striptags(event.announce)), 30)
        d['image'] =event.event_image.image.url if event.event_image else settings.STATIC_URL + "www/images/img-upcoming.gif"
        eventss.append(d)

    ret = dict()
    ret['events'] = eventss
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), mimetype='application/json')

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
    event_url = urlparse.urlparse(event.get_absolute_url()).path
    if not request.path.endswith(event_url):
        return HttpResponseRedirect(event.get_absolute_url())

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
    cal = icalendar.Calendar()
    cal.add('prodid', '-//Kiberpipa//NONSGML intranet//EN')
    cal.add('version', '2.0')

    events = Event.objects.order_by('-chg_date')[:20]

    for e in events:
        if e.public:
            classification = u'PUBLIC'
        else:
            continue
        cal_event = icalendar.Event()
        cal_event.add('uid', u'UID:event-%s@kiberpipa.org' % e.id)
        cal_event.add('summary', u'%s: %s' % (e.project, e.title))
        cal_event.add('url', u'http://www.kiberpipa.org%s' % e.get_absolute_url())
        cal_event.add('location', e.place.name)
        cal_event.add('classification', classification)
        cal_event.add('sequence', e.sequence)
        cal_event.add('categories', u','.join([e.project.name, e.category.name]))
        # http://www.kanzaki.com/docs/ical/transp.html
        cal_event.add('transp', 'OPAQUE')
        # dtstamp means when was the last time icalendar feed has changed
        cal_event.add('dtstamp', ljubljana_tz.localize(datetime.datetime.now()))
        cal_event.add('dtstart', ljubljana_tz.localize(e.start_date))
        cal_event.add('dtend', ljubljana_tz.localize(e.end_date))
        cal_event.add('last-modified', ljubljana_tz.localize(e.chg_date))
        organizer = icalendar.vCalAddress(u'MAILTO:info@kiberpipa.org')
        organizer.params['cn'] = u'Kiberpipa'
        cal_event.add('organizer', organizer)
        cal.add_component(cal_event)

    response = HttpResponse(mimetype='text/calendar; charset=UTF-8')
    response.write(cal.to_ical())
    return response


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


# TODO: use locale aware flatpages for this
def press(request):
    if request.LANGUAGE_CODE == 'en':
        template = 'www/press_en.html'
    else:
        template = 'www/press.html'
    return render_to_response(template, RequestContext(request, {}))


def location(request):
    if request.LANGUAGE_CODE == 'en':
        template = 'www/kjesmo_en.html'
    else:
        template = 'www/kjesmo.html'
    return render_to_response(template, RequestContext(request, {}))


class NewsList(ListView):
    template_name = 'www/news_list.html'
    queryset = News.objects.order_by('-date')
    paginate_by = 10

    def get_queryset(self):
        if self.request.LANGUAGE_CODE == 'en':
            return self.queryset.filter(language='en')
        else:
            return self.queryset
