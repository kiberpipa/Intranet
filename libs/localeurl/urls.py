from django.conf.urls.defaults import *
from localeurl.views import change_locale

urlpatterns = patterns('',
	url(r'^change/', change_locale, name='localeurl_change_locale'),
)
