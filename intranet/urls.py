from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import ListView
from feedjack.models import Post


urlpatterns = patterns('',
    (r'^', include('intranet.www.urls')),
    (r'^intranet/', include('intranet.org.urls')),
    (r'^gallery/', include('pipa.gallery.urls')),
    (r'^services/ltsp/', include('pipa.ltsp.urls')),
    (r'^planet/', ListView.as_view(queryset=Post.objects.order_by('-date_modified')[:30])),

    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),

    (r'^grappelli/', include('grappelli.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
