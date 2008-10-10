from django.conf.urls.defaults import *

from intranet.www.models import News

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^event/(?P<slug>[-\w]+)$', 'intranet.www.views.event'),
    url(r'^event/next/(?P<position>[\d-]+)/(?P<offset>[\d-]+)/(?P<num>\d+)/$', 'intranet.www.views.timeline_events'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^calendar/ical/', 'intranet.www.views.ical'),
    url(r'^calendar/', 'intranet.www.views.calendar'),
    url(r'^index\.php', 'intranet.www.views.compat'),
)
