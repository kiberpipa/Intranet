from django.conf.urls.defaults import *
from intranet.kapelica.models import Event, General

event_dict = {
    'queryset': Event.objects.all(),
    'date_field': 'start_date',
    'allow_empty': 1,
    'allow_future': 1,
}

event_detail = {
    'queryset': Event.objects.all(),
}

page_detail = {
    'queryset': General.objects.all(),
    'slug_field': 'slug',
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'events/'}),
    #'intranet.kapelica.views.index'),
    (r'^pages/edit/(?P<id>\d+)', 'intranet.kapelica.views.edit_page'),
    (r'^pages/add/$', 'intranet.kapelica.views.create_page'),
    (r'^pages/$', 'intranet.kapelica.views.kb_index'),
    (r'^events/create/', 'intranet.kapelica.views.create_event'),
    (r'^events/(\d+)/edit/$', 'intranet.kapelica.views.edit_event'),
    (r'^events/$', 'intranet.kapelica.views.events', event_dict),
)

urlpatterns += patterns('django.views.generic.date_based',
    (r'events/archive/(?P<year>\d{4})/$',	'archive_year',  event_dict),
#    (r'events/$',	'archive_index', event_dict),
)

urlpatterns += patterns('django.views.generic.list_detail',
    (r'events/(?P<object_id>\d+)', 'object_detail', event_detail),
    (r'pages/(?P<slug>\w+)', 'object_detail', page_detail),
)
