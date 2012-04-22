from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import ListView, TemplateView
from feedjack.models import Post


urlpatterns = patterns('',
    (r'^intranet/', include('intranet.org.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^services/ltsp/', include('pipa.ltsp.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^comments/post/$', 'intranet.www.views.anti_spam'),
    url(r'^ajax/index/events/$', 'intranet.www.views.ajax_index_events'),
    url(r'^ajax/add_mail/(?P<event>[0-9]+)/(?P<email>[^/]*)$', 'intranet.www.views.ajax_add_mail'),
    url(r'^ajax/subscribe_mailinglist/', 'intranet.www.views.ajax_subscribe_mailinglist', name="ajax_subscribe_mailinglist"),
    url(r'^rss/$', TemplateView.as_view(template_name='www/rss.html'), name="rss"),
)

urlpatterns += i18n_patterns('',
    (r'^', include('intranet.www.urls')),
    (r'^gallery/', include('pipa.gallery.urls')),
    (r'^planet/', ListView.as_view(queryset=Post.objects.order_by('-date_modified')[:30])),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
