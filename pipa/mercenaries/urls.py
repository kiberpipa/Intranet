from django.conf.urls import patterns

urlpatterns = patterns('pipa.mercenaries.views',
    (r'^$', 'index'),
    (r'^(?P<year>\d*)/(?P<month>\d*)/$', 'index'),
    (r'^(?P<year>\d*)/(?P<month>\d*)/(?P<id>\d+|napotnice|redni)/$', 'export_xls'),
)
