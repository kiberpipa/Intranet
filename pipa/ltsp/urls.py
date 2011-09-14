from django.conf.urls.defaults import *

urlpatterns = patterns('pipa.ltsp.service',
    (r'^background.png', 'ltsp_background_image'),
    (r'^usage/', 'internet_usage_report'),
)
