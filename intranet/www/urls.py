from django.conf.urls.defaults import *

from intranet.www.models import News
from intranet.org.models import Alumni

alumni_dict = {
    'queryset': Alumni.objects.all(),
    'template_name': 'www/alumni.html',
}

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^event/(?P<slug>[-\w]+)$', 'intranet.www.views.event'),
    #url(r'^event/next/(?P<position>[\d-]+)/(?P<offset>[\d-]+)/(?P<num>\d+)/$', 'intranet.www.views.timeline_events'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^calendar/ical/?(?P<month>month)?/?$', 'intranet.www.views.ical'),
    url(r'^calendar/', 'intranet.www.views.calendar'),
    url(r'^index\.php', 'intranet.www.views.compat'),
    url(r'^alumni/', 'django.views.generic.list_detail.object_list', alumni_dict),
)
