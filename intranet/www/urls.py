from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^rss/?$', 'intranet.www.views.rss'),
    url(r'^event/(?P<date>\d{4}-[a-z]{3}-[0-9]{1,2})/(?P<id>\d+)/(?P<slug>[-\w]+)/?$', 'intranet.www.views.event'),
    url(r'^news/$', 'intranet.www.views.news_list'),
    url(r'^news/(?P<id>\d+)/(?P<slug>[-\w]+)/?$', 'intranet.www.views.news_detail'),
    url(r'^news/(?P<slug>[-\w]+)/?$', 'intranet.www.views.news_detail'),
    url(r'^calendar/ical/$', 'intranet.www.views.ical'),
    url(r'^calendar/(?P<year>\d+)?/?(?P<month>\d+)?/?', 'intranet.www.views.calendar'),
    url(r'^(modules|index)\.php', 'intranet.www.views.compat'),
    url(r'^alumni/', 'pipa.addressbook.views.alumni'),
    url(r'^press/', 'intranet.www.views.press'),
    url(r'^locale/?$', 'django.views.generic.simple.direct_to_template', {'template': 'www/locale.html'}),
    url(r'^ajax/index/events/$', 'intranet.www.views.ajax_index_events'),
    url(r'^ajax/add_mail/(?P<event>[0-9]+)/(?P<email>[^/]*)$', 'intranet.www.views.ajax_add_mail'),

    #backwards compatibility
    url(r'^press-en/', 'django.views.generic.simple.redirect_to', {'url': '/en/press/'},),
    url(r'^alumni-en/', 'django.views.generic.simple.redirect_to', {'url': '/en/alumni/'},),
    url(r'^calendar-en/', 'django.views.generic.simple.redirect_to', {'url': '/en/calendar/'},),
)
