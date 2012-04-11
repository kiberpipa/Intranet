from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView, TemplateView
from haystack.query import SearchQuerySet

from intranet.org.models import Place, Event
from intranet.www.feeds import AllInOne, NewsFeed, EventsFeed, POTFeed, SUFeed, VIPFeed, PlanetFeed, MuzejFeed


urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^rss/$', 'intranet.www.views.rss', name="rss"),
    url(r'^event/(?P<slug>[-\w]*)-(?P<id>\d+)/', 'intranet.www.views.event', name="event_detail"),
    url(r'^event/search/', 'haystack.views.basic_search', dict(
        template='search/search_event.html',
        searchqueryset=SearchQuerySet().models(Event).filter(is_public=True),
        ), name="event_search"),
    url(r'^news/$', 'intranet.www.views.news_list'),
    url(r'^news/comments/post/$', 'intranet.www.views.anti_spam'),
    url(r'^news/(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'intranet.www.views.news_detail'),
    url(r'^news/(?P<id>\d+)/$', 'intranet.www.views.news_detail'),
    url(r'^news/(?P<slug>[-\w]+)/$', 'intranet.www.views.news_detail'),
    url(r'^calendar/$', 'intranet.www.views.calendar'),
    url(r'^calendar/ical/$', 'intranet.www.views.ical'),
    url(r'^calendar/(?P<year>\d{4})/(?P<month>[0-1]?[0-9])?', 'intranet.www.views.calendar'),
    url(r'^prostori/$', 'intranet.www.views.facilities'),
    url(r'^prostori/(?P<object_id>\d+)/opis.ajax$', 'django.views.generic.list_detail.object_detail',
        {'template_name': 'www/facility_description_ajax.html',
        'queryset': Place.objects.all()}, name="facility_description_ajax"),
    url(r'^locale/$', TemplateView.as_view(template_name='www/locale.html')),
    url(r'^kjesmo/$', TemplateView.as_view(template_name='www/kjesmo.html')),
    url(r'^alumni/', 'pipa.addressbook.views.alumni'),
    url(r'^press/', 'intranet.www.views.press'),

    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^comments/post/$', 'intranet.www.views.anti_spam'),

    # ajax
    url(r'^ajax/index/events/$', 'intranet.www.views.ajax_index_events'),
    url(r'^ajax/add_mail/(?P<event>[0-9]+)/(?P<email>[^/]*)$', 'intranet.www.views.ajax_add_mail'),
    url(r'^ajax/subscribe_mailinglist/', 'intranet.www.views.ajax_subscribe_mailinglist', name="ajax_subscribe_mailinglist"),

    # feeds
    (r'^feeds/all/', AllInOne()),
    (r'^feeds/novice/', NewsFeed()),
    (r'^feeds/dogodki/', EventsFeed()),
    (r'^feeds/pot/', POTFeed()),
    (r'^feeds/su/', SUFeed()),
    (r'^feeds/vip/', VIPFeed()),
    (r'^feeds/planet/', PlanetFeed()),
    (r'^feeds/muzej/', MuzejFeed()),

    # backwards compatibility
    url(r'^press-en/', RedirectView.as_view(url='/en/press/', permanent=True)),
    url(r'^alumni-en/', RedirectView.as_view(url='/en/alumni/', permanent=True)),
    url(r'^calendar-en/', RedirectView.as_view(url='/en/calendar/', permanent=True)),
    url(r'^event/\d{4}-[a-z]{3}-[0-9]{1,2}/(?P<id>\d+)/(?P<slug>[-\w]*)',
        RedirectView.as_view(url='event/%(slug)s-%(id)s/', permanent=True)),
)
