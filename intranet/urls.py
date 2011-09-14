from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.conf import settings
from feedjack.models import Post

from intranet.www.feeds import *


planet_dict = {
    'queryset': Post.objects.order_by('-date_modified')[:30],
}

feeds = {
    'all': AllInOne,
    'novice': NewsFeed,
    'dogodki': EventsFeed,
    'pot': POTFeed,
    'su': SUFeed,
    'vip': VIPFeed,
    'planet': PlanetFeed,
    'muzej': MuzejFeed,
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

    # keep this here as a way to force normalization of feeds
    (r'^feeds/(?P<feed>%s)/.+$' % '|'.join(feeds.keys()),
        'django.views.generic.simple.redirect_to', {'url': '/sl/feeds/%(feed)s/', 'permanent': True}),
    (r'^feeds/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    (r'^grappelli/', include('grappelli.urls')),
    (r'^sentry/', include('sentry.web.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
