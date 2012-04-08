from django.conf.urls import patterns

urlpatterns = patterns('pipa.ltsp.service',
    (r'^background.png', 'ltsp_background_image'),
    (r'^usage/', 'internet_usage_report'),
)
