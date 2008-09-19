from django.conf.urls.defaults import *

from intranet.www.models import News

urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
    url(r'^event/(?P<slug>[-\w]+)$', 'intranet.www.views.event'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^news/(?P<slug>[-\w]+)$', 'intranet.www.views.news'),
    url(r'^index\.php', 'intranet.www.views.compat'),
)
