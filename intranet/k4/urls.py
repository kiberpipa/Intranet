from django.conf.urls.defaults import *

from intranet.k4.models import Event

event_dict = {
    'queryset': Event.objects.all(),
    'date_field': 'start_date',
    'allow_empty': 1,
    'allow_future': 1,
}

event_detail = {
    'queryset': Event.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'intranet.k4.views.index', {'url': 'events/'}),
    (r'^events/create/', 'intranet.k4.views.create_event'),
    (r'^events/(\d+)/edit/$', 'intranet.k4.views.edit_event'),
    (r'^events/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', event_detail),
    (r'^events/$',	'django.views.generic.date_based.archive_index', event_dict),
)

