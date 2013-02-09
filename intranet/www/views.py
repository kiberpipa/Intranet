# *-* coding: utf-8 *-*

import datetime
import logging
import urllib2
import urlparse
import simplejson
from calendar import Calendar

import icalendar
import pytz
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.defaultfilters import striptags, safe, truncatewords
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
from django_mailman.models import List
from feedjack.models import Post
from haystack.query import SearchQuerySet
import twitter

from intranet.org.models import Event, Email
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


# TODO: http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
#@cache_page(5 * 60)
def index(request):
    """
        Load everything we need for the frontpage
        And that's a lot of stuff

    """
    # load news items (internal) and blog posts (members' blogs, fetched via rss)
    news = News.objects.order_by('-date')[:4]
    posts = Post.objects.order_by('-date_modified')[:4]
    videos = Video.objects.order_by('-pub_date')[:5]

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

    # load some tweets
    api = twitter.Api()
    tweets = api.GetSearch(term='kiberpipa OR cyberpipe')

    # recent flickr uploads
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
        'both': both2,
        'videos': videos,
        'tweets': tweets,
        'pictures': pictures,
    }, context_instance=RequestContext(request))


def ajax_index_events(request, year=None, week=None):
    today = datetime.date.today()
    week = int(week or today.isocalendar()[1])
    year = int(year or today.year)

    # %Y: year,
    # %W: week of the year (starting with first monday of the year),
    # %w: weekday (0 being sunday)
    start = week_start_date(year, week)
    end = start + relativedelta(days=7)

    # get all events in this week
    # TODO: this will fail for events that last more than a week
    # TODO: for this purpose, we should just use postgres daterange sooner or later.
    q = Event.objects.filter(public=True,
                             start_date__range=(start, end),
                             end_date__range=(start, end))
    events = q.order_by('start_date').all()

    # figure out if we are streaming now
    streaming_event = None
    if week == int(today.isocalendar()[1]) and is_streaming():
        try:
            now = datetime.datetime.now()
            streaming_event = Event.objects.filter(public=True,
                                                   start_date__lte=now).order_by('-start_date')[0]
            next_event = streaming_event.get_next()
            td = next_event.start_date - now
            if td.days == 0 and 0 < td.seconds < 1800:
                # if there is 30min to next event, take that one
                streaming_event = next_event
            # TODO: if previous event should have ended more than 3 hours ago, don't display the stream
        except IndexError:
            pass

    # TODO: a bug with calculating week number
    prev_week_date = start - relativedelta(days=7)
    next_week_date = start + relativedelta(days=7)
    ret = dict()
    ret['prev_url'] = reverse('ajax_events_week', kwargs=dict(year=prev_week_date.isocalendar()[0], week=prev_week_date.isocalendar()[1]))
    ret['next_url'] = reverse('ajax_events_week', kwargs=dict(year=next_week_date.isocalendar()[0], week=next_week_date.isocalendar()[1]))
    ret['events'] = {}

    dict_events = []

    for event in events:
        d = dict(id=event.id,
                 title=event.title,
                 start_date=event.start_date,
                 end_date=event.end_date,
                 place=event.place.name,
                 url=event.get_absolute_url())
        d['project'] = event.project.verbose_name or event.project.name
        d['announce'] = truncatewords(safe(striptags(event.announce)), 50)
        d['image'] = event.event_image.image.url
        if streaming_event:
            d['is_streaming'] = streaming_event.id == event.id
        else:
            d['is_streaming'] = False
        dict_events.append(d)

    # group by events with the days in a week
    for i, day in enumerate(map(lambda i: start + relativedelta(days=i), range(0, 7))):
        ret['events'][i] = dict(
            date=day.strftime('%a, %d. %b'),
            events=[],
            is_today=day == today,
        )
        for event in dict_events:
            start_date = datetime.date(event['start_date'].year, event['start_date'].month, event['start_date'].day)
            end_date = datetime.date(event['end_date'].year, event['end_date'].month, event['end_date'].day)
            # TODO: order of events is wrong
            if start_date <= day <= end_date:
                ret['events'][i]['events'].append(event)
                # TODO: note if event hasnt started today

    return HttpResponse(simplejson.dumps(ret, cls=DjangoJSONEncoder),
                        mimetype='application/json')


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


def calendar_dayclass(date, month):
    # stuff needed to determine date class
    # like today's date, the first day of next month, or the last day of the previous one
    today = datetime.date.today()
    next_month = month + relativedelta(months=1)
    next_month = datetime.date(next_month.year, next_month.month, 1)
    prev_month = datetime.date(month.year, month.month, 1) - relativedelta(days=1)

    if date == today:
        return 'today'
    elif date >= next_month:
        return 'next-month'
    elif date <= prev_month:
        return 'prev-month'
    elif date < today:
        return 'past-in-this-month'
    elif date > today:
        return 'future-in-this-month'


def calendar(request, year=None, month=None, en=False):
    today = datetime.date.today()
    year = int(year or today.year)
    month = int(month or today.month)
    now = datetime.date(year, month, 15)
    cal = Calendar().monthdatescalendar(year, month)
    events = []

    for week in cal:
        for day in week:
            events.append([day, calendar_dayclass(day, now), Event.objects.filter(start_date__year=day.year, start_date__month=day.month, start_date__day=day.day).order_by('start_date')])

    next_month = now + relativedelta(months=+1)
    prev_month = now + relativedelta(months=-1)

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
            text = get_template('mail/facilities_request.txt').render(
                Context(form.cleaned_data))
            send_mail("Povpraševanje o prostorih",
                      text,
                      settings.DEFAULT_FROM_EMAIL, ['info@kiberpipa.org'])
            done = _(u'Your rental inquiry has been sent. We will answer it in a couple of work days')  # NOQA
    else:
        form = EventContactForm()
    return render_to_response('www/facilities.html',
                              RequestContext(request, locals()))


def about(request):
    if request.LANGUAGE_CODE == 'en':
        template = 'www/about_en.html'
    else:
        template = 'www/about.html'
    return render_to_response(template, RequestContext(request, {}))


# TODO: use locale aware flatpages for this
def press(request):
    if request.LANGUAGE_CODE == 'en':
        template = 'www/press_en.html'
    else:
        template = 'www/press.html'
    return render_to_response(template, RequestContext(request, {}))


def support(request):
    template = 'www/support.html'
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


def week_start_date(year, week):
    """Calculate week start date from ISO week.
    Taken from http://stackoverflow.com/a/1287862/133235
    """
    d = datetime.date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = datetime.timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta
