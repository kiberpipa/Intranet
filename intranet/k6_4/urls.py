from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'k6_4/index.html'}),
#    (r'^events/create/', 'intranet.k6_4.views.create_event'),
#    (r'^events/(\d+)/edit/$', 'intranet.k6_4.views.edit_event'),
#    (r'^events/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', event_detail),
#    (r'events/$',	'django.views.generic.date_based.archive_index', event_dict),
)

