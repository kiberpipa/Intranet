from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from intranet.photologue.models import *
from intranet.feedjack.models import Post

admin.autodiscover()

SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)
gallery_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}

planet_dict = {
    'queryset': Post.objects.order_by('-date_created')[:30],
}

urlpatterns = patterns('',
    #(r'^video3/', include('intranet.video.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^intranet/', include('intranet.org.urls')),
    (r'^intranet/wiki/', include('intranet.wiki.urls')),
    (r'^', include('intranet.www.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/intranet/admin'}),
    (r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': 'login/'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    #(r'^planet/', include('intranet.feedjack.urls')),
    (r'^planet/', 'django.views.generic.list_detail.object_list', planet_dict),


    (r'^gallery/', include('intranet.photologue.urls')),

    (r'^intranet/admin/(.*)', admin.site.root),
)

if settings.DEBUG:
  from intranet.settings import next_to_this_file
  urlpatterns += patterns('',
    (r'^smedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root':   next_to_this_file(__file__, '../media')}),
    (r'^amedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root':   next_to_this_file(__file__, '../admin-media')}),
  )
