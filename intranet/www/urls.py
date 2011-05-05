from django.conf.urls.defaults import *

from intranet.org.models import Place

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^rss/$', 'intranet.www.views.rss', name="rss"),
    url(r'^event/(?P<date>\d{4}-[a-z]{3}-[0-9]{1,2})/(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'intranet.www.views.event'),
    url(r'^news/$', 'intranet.www.views.news_list'),
    url(r'^news/comments/post/$', 'intranet.www.views.anti_spam'),
    url(r'^news/(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'intranet.www.views.news_detail'),
    url(r'^news/(?P<id>\d+)/$', 'intranet.www.views.news_detail'),
    url(r'^news/(?P<slug>[-\w]+)/$', 'intranet.www.views.news_detail'),
    url(r'^calendar/ical/$', 'intranet.www.views.ical'),
    url(r'^calendar/$', 'intranet.www.views.calendar'),
    url(r'^calendar/(?P<year>\d{4})/(?P<month>[0-1]?[0-9])?', 'intranet.www.views.calendar'),
    url(r'^alumni/', 'pipa.addressbook.views.alumni'),
    url(r'^press/', 'intranet.www.views.press'),
    url(r'^prostori/$', 'intranet.www.views.facilities'),
    url(r'^prostori/(?P<object_id>\d+)/opis.ajax$', 'django.views.generic.list_detail.object_detail',
        {'template_name': 'www/facility_description_ajax.html',
        'queryset': Place.objects.all(),}, name="facility_description_ajax"),
    url(r'^locale/$', 'django.views.generic.simple.direct_to_template', {'template': 'www/locale.html'}),
    url(r'^kjesmo/$', 'django.views.generic.simple.direct_to_template', {'template': 'www/kjesmo.html'}),
    url(r'^odjava/$', 'intranet.www.views.odjava'),

    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^comments/post/$', 'intranet.www.views.anti_spam'),

    # ajax
    url(r'^ajax/index/events/$', 'intranet.www.views.ajax_index_events'),
    url(r'^ajax/add_mail/(?P<event>[0-9]+)/(?P<email>[^/]*)$', 'intranet.www.views.ajax_add_mail'),

    # backwards compatibility
    url(r'^press-en/', 'django.views.generic.simple.redirect_to', {'url': '/en/press/'},),
    url(r'^alumni-en/', 'django.views.generic.simple.redirect_to', {'url': '/en/alumni/'},),
    url(r'^calendar-en/', 'django.views.generic.simple.redirect_to', {'url': '/en/calendar/'},),
)
