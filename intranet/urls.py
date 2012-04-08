from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.conf import settings
from feedjack.models import Post

from intranet.www.feeds import *


planet_dict = {
    'queryset': Post.objects.order_by('-date_modified')[:30],
}


js_info_dict = {
    'packages': ('intranet.www', 'intranet.org'),
}

urlpatterns = patterns('',
    (r'^', include('intranet.www.urls')),
    (r'^intranet/', include('intranet.org.urls')),
    (r'^gallery/', include('pipa.gallery.urls')),
    (r'^services/ltsp/', include('pipa.ltsp.urls')),
    (r'^planet/', 'django.views.generic.list_detail.object_list', planet_dict),

    (r'^feeds/all/', AllInOne()),
    (r'^feeds/novice/', NewsFeed()),
    (r'^feeds/dogodki/', EventsFeed()),
    (r'^feeds/pot/', POTFeed()),
    (r'^feeds/su/', SUFeed()),
    (r'^feeds/vip/', VIPFeed()),
    (r'^feeds/planet/', PlanetFeed()),
    (r'^feeds/muzej/', MuzejFeed()),

    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    (r'^grappelli/', include('grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
