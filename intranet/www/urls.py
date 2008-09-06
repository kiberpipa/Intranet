from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^event/(?P<id>\d+)$', 'intranet.www.views.event'),
)
