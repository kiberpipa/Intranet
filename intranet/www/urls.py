from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^$', 'intranet.www.views.index'),
)
