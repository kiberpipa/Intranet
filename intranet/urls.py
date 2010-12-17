from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from feedjack.models import Post

from pipa.ldap.forms import LoginForm
from intranet.www.feeds import *

admin.autodiscover()

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
    'packages': ('intranet.www', 'intranet.org', 'intranet.web', 'intranet.wiki'),
}

urlpatterns = patterns('',
    (r'^', include('intranet.www.urls')),
    (r'^intranet/', include('intranet.org.urls')),
    url(r'^intranet/ldappass/', 'pipa.ldap.views.password_change', name='ldap_password_change'),
    (r'^intranet/oldwiki/', include('intranet.wiki.urls')),
    (r'^accounts/login/$', 'pipa.ldap.views.login', {'authentication_form': LoginForm}),
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/intranet/admin'}),
    (r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': 'login/'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    (r'^planet/', 'django.views.generic.list_detail.object_list', planet_dict),

    # keep this here as a way to force normalization of feeds
    (r'^feeds/(?P<feed>%s)/.+$' % '|'.join(feeds.keys()),
        'django.views.generic.simple.redirect_to', {'url': '/sl/feeds/%(feed)s/', 'permanent': True}),
    (r'^feeds/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),


    (r'^intranet/admin/(.*)', admin.site.root),
    (r'^news/comments/post/$', 'intranet.www.views.anti_spam'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^comments/post/$', 'intranet.www.views.anti_spam'),

    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    (r'services/ltsp/', include('pipa.ltsp.urls')),
)

if settings.DEBUG:
    from intranet.settings import next_to_this_file
    urlpatterns += patterns('',
        (r'^smedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^amedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root':   next_to_this_file(__file__, '../admin-media')}),
    )
