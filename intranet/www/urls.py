from django.conf.urls.defaults import *

from intranet.www.models import News
from intranet.org.models import Alumni, Clipping, Event

alumni_dict = {
    'queryset': Alumni.objects.all(),
    'template_name': 'www/alumni.html',
}

alumni_dict_en = {
    'queryset': Alumni.objects.all(),
    'template_name': 'www/alumni-en.html',
}

press_dict = {
    'queryset': Clipping.objects.order_by('-date')[:15],
}

press_dict_en = {
    'queryset': Clipping.objects.order_by('-date')[:15],
    'template_name': 'www/press-en.html',
}

news_en_dict = {
    'queryset': Event.objects.filter(language='EN'),
    'template_name': 'www/news-en.html',
}

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^rss/?$', 'intranet.www.views.rss'),
    #url(r'^event/(?P<slug>[-\w]+)$', 'intranet.www.views.event'),
    url(r'^event/\d{4}-[a-z]{3}-[0-9]{1,2}/(?P<id>\d+)/[-\w]+/?$', 'intranet.www.views.event'),
    #url(r'^event/next/(?P<position>[\d-]+)/(?P<offset>[\d-]+)/(?P<num>\d+)/$', 'intranet.www.views.timeline_events'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^calendar/ical/?(?P<month>month)?/?$', 'intranet.www.views.ical'),
    url(r'^calendar/(?P<year>\d+)?/?(?P<month>\d+)?/?', 'intranet.www.views.calendar'),
    url(r'^calendar-en/', 'intranet.www.views.calendar', {'en': True}),
    url(r'^(modules|index)\.php', 'intranet.www.views.compat'),
    url(r'^alumni/', 'django.views.generic.list_detail.object_list', alumni_dict),
    url(r'^news-en/', 'django.views.generic.list_detail.object_list', news_en_dict),
    url(r'^alumni-en/', 'django.views.generic.list_detail.object_list', alumni_dict_en),
    url(r'^press/', 'django.views.generic.list_detail.object_list', press_dict),
    url(r'^press-en/', 'django.views.generic.list_detail.object_list', press_dict_en),
    url(r'^ajax/gallery/(?P<id>\d+|[\w-]+)/$', 'intranet.www.views.gallery'),
)
