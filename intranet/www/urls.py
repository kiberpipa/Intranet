from django.conf.urls.defaults import *

from intranet.www.models import News
from intranet.org.models import Alumni, Clipping

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

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^rss/?$', 'intranet.www.views.rss'),
    url(r'^event/(?P<slug>[-\w]+)$', 'intranet.www.views.event'),
    #url(r'^event/next/(?P<position>[\d-]+)/(?P<offset>[\d-]+)/(?P<num>\d+)/$', 'intranet.www.views.timeline_events'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^calendar/ical/?(?P<month>month)?/?$', 'intranet.www.views.ical'),
    url(r'^calendar/', 'intranet.www.views.calendar'),
    url(r'^index\.php', 'intranet.www.views.compat'),
    url(r'^alumni/', 'django.views.generic.list_detail.object_list', alumni_dict),
    url(r'^alumni-en/', 'django.views.generic.list_detail.object_list', alumni_dict_en),
    url(r'^press/', 'django.views.generic.list_detail.object_list', press_dict),
    url(r'^ajax/gallery/(?P<id>\d+|[\w-]+)/$', 'intranet.www.views.gallery'),
)
