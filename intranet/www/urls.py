from django.conf.urls import patterns, url
from django.views.generic import RedirectView, TemplateView, DetailView
from haystack.query import SearchQuerySet

from intranet.org.models import Place, Event
from intranet.www.feeds import AllInOne, NewsFeed, EventsFeed, POTFeed, SUFeed, VIPFeed, PlanetFeed, MuzejFeed
from intranet.www.views import NewsList


urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index', name="index"),
    url(r'^event/(?P<slug>[-\w]*)-(?P<id>\d+)/$', 'intranet.www.views.event', name="event_detail"),
    url(r'^event/\d{4}-[a-z]{3}-[0-9]{1,2}/(?P<id>\d+)/(?P<slug>[^/]*)',
        RedirectView.as_view(url='/event/%(slug)s-%(id)s/', permanent=True)),
    url(r'^event/search/', 'haystack.views.basic_search', dict(
        template='search/search_event.html',
        searchqueryset=SearchQuerySet().models(Event).filter(is_public=True),
        ), name="event_search"),
    url(r'^news/$', NewsList.as_view(), name="news"),
    url(r'^news/comments/post/$', 'django.contrib.comments.views.comments.post_comment'),
    url(r'^news/(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'intranet.www.views.news_detail'),
    url(r'^news/(?P<id>\d+)/$', 'intranet.www.views.news_detail'),
    url(r'^news/(?P<slug>[-\w]+)/$', 'intranet.www.views.news_detail'),
    url(r'^calendar/$', 'intranet.www.views.calendar', name="calendar"),
    url(r'^calendar/(?P<year>\d{4})/(?P<month>[0-1]?[0-9])?', 'intranet.www.views.calendar'),
    url(r'^calendar/ical/$', 'intranet.www.views.ical', name="calendar_ical"),
    url(r'^prostori/$', 'intranet.www.views.facilities'),
    url(r'^prostori/(?P<pk>\d+)/opis.ajax$', DetailView.as_view(
        queryset=Place.objects.all(),
        template_name="www/facility_description_ajax.html",
    ), name="facility_description_ajax"),
    url(r'^alumni/', 'pipa.addressbook.views.alumni'),
    # TODO: migrate press to flatpages
    url(r'^press/', 'intranet.www.views.press'),
    url(r'^about/', 'intranet.www.views.about'),

    # converted flatpages to custom templates with some flatpage includes
    url(r'^support/', 'intranet.www.views.support'),

    # feeds
    (r'^feeds/all/', AllInOne()),
    (r'^feeds/novice/', NewsFeed()),
    (r'^feeds/dogodki/', EventsFeed()),
    (r'^feeds/pot/', POTFeed()),
    (r'^feeds/su/', SUFeed()),
    (r'^feeds/planet/', PlanetFeed()),
    (r'^feeds/muzej/', MuzejFeed()),

    # backwards compatibility
    url(r'^press-en/', RedirectView.as_view(url='/en/press/', permanent=True)),
    url(r'^alumni-en/', RedirectView.as_view(url='/en/alumni/', permanent=True)),
    url(r'^calendar-en/', RedirectView.as_view(url='/en/calendar/', permanent=True)),
)
