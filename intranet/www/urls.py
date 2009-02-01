from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^rss/?$', 'intranet.www.views.rss'),
    #url(r'^event/(?P<slug>[-\w]+)$', 'intranet.www.views.event'),
    url(r'^event/\d{4}-[a-z]{3}-[0-9]{1,2}/(?P<id>\d+)/[-\w]+/?$', 'intranet.www.views.event'),
    #url(r'^event/next/(?P<position>[\d-]+)/(?P<offset>[\d-]+)/(?P<num>\d+)/$', 'intranet.www.views.timeline_events'),
    #url(r'^news/?$', 'django.views.generic.list_detail.object_list', news_list),
    url(r'^news/', 'intranet.www.views.news_list'),
    url(r'^news/(?P<slug>[-\w]+)/?$', 'intranet.www.views.news_detail'),
    url(r'^calendar/ical/?(?P<month>month)?/?$', 'intranet.www.views.ical'),
    url(r'^calendar/(?P<year>\d+)?/?(?P<month>\d+)?/?', 'intranet.www.views.calendar'),
    url(r'^(modules|index)\.php', 'intranet.www.views.compat'),
    url(r'^alumni/', 'intranet.www.views.alumni'),
    url(r'^press/', 'intranet.www.views.press'),
    url(r'^locale/?$', 'django.views.generic.simple.direct_to_template', {'template': 'www/locale.html'}),
    url(r'^ajax/gallery/(?P<id>\d+|[\w-]+)/$', 'intranet.www.views.gallery'),
    url(r'^ajax/index/events/$', 'intranet.www.views.ajax_index_events'),
    url(r'^ajax/add_mail/(?P<event>[0-9]+)/(?P<email>[^/]*)$', 'intranet.www.views.ajax_add_mail'),
)

# URL-ji potrebni redirecta po deployu
#url(r'^press-en/', 'django.views.generic.list_detail.object_list', press_dict_en),
#url(r'^alumni-en/', 'django.views.generic.list_detail.object_list', alumni_dict),
#url(r'^calendar-en/', 'intranet.www.views.calendar', {'en': True}),


