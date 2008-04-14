from django.conf.urls.defaults import *
from intranet.video.models import Video, VideoCategory

event_dict = {
    'queryset': Video.objects.all(),
    'date_field': 'date',
    'allow_empty': 1,
    'allow_future': 1,
}

event_year = {
    'queryset': Video.objects.all(),
    'date_field': 'date',
    'allow_empty': 1,
    'allow_future': 1,
    'make_object_list': 1,
}

urlpatterns = patterns('',
#    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'video/index.html'}),
#    (r'^events/create/', 'intranet.k6_4.views.create_event'),
#    (r'^events/(\d+)/edit/$', 'intranet.k6_4.views.edit_event'),
#    (r'^events/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', event_detail),
    (r'^upload/$', 'intranet.video.views.upload'),
    (r'^(\w+)/$', 'intranet.video.views.cat_index'),
)

urlpatterns += patterns('django.views.generic.date_based',
    (r'^$',    'archive_index', event_dict),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',    'archive_month', event_dict),
    (r'^(?P<year>\d{4})/$',    'archive_year',  event_year),
)

