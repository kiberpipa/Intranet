from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

#from intranet.photologue.models import *
from intranet.feedjack.models import Post
from intranet.www.feeds import *

admin.autodiscover()

SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)
#gallery_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}

planet_dict = {
    'queryset': Post.objects.order_by('-date_modified')[:30],
}

feeds = {
    'all': AllInOne,
}

js_info_dict = {
    'packages': ('intranet.www', 'intranet.org', 'intranet.web', 'intranet.tags', 'intranet.wiki'),
}

urlpatterns = patterns('',
    #(r'^video3/', include('intranet.video.urls')),
    (r'^intranet/', include('intranet.org.urls')),
    (r'^intranet/wiki/', include('intranet.wiki.urls')),
    (r'^', include('intranet.www.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/intranet/admin'}),
    (r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': 'login/'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    #(r'^planet/', include('intranet.feedjack.urls')),
    (r'^planet/', 'django.views.generic.list_detail.object_list', planet_dict),

    (r'^feeds/(?P<url>.*)', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    #(r'^gallery/', include('intranet.photologue.urls')),

    (r'^intranet/admin/(.*)', admin.site.root),
    (r'^comments/post/$', 'intranet.www.views.anti_spam'),
    (r'^news/comments/post/$', 'intranet.www.views.anti_spam'),
    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)

if settings.DEBUG:
  from intranet.settings import next_to_this_file
  urlpatterns += patterns('',
    (r'^smedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root':   next_to_this_file(__file__, '../media')}),
    #for shorter urls
    (r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root':   next_to_this_file(__file__, '../media/photologue/photos')}),
    (r'^amedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root':   next_to_this_file(__file__, '../admin-media')}),
  )
