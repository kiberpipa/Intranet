from django.conf.urls.defaults import *
from django.conf import settings
#from django.contrib import admin

urlpatterns = patterns('',
    #(r'^video3/', include('intranet.video.urls')),
    (r'^intranet/', include('intranet.org.urls')),
    (r'^intranet/wiki/', include('intranet.wiki.urls')),
    #(r'^kiberpipa/', include('intranet.web.urls')),
    #(r'^kapelica/', include('intranet.kapelica.urls')),
#    (r'^slotechart/', include('intranet.slotechart.urls')),
#    (r'^zavod/', include('intranet.k6_4.urls')),
#    (r'^k4/', include('intranet.k4.urls')),
    #(r'^bruc06/', include('intranet.bruc06.urls')),

    # Uncomment this for admin:
    (r'^intranet/admin/', include('django.contrib.admin.urls')),
     #(r'^intranet/admin/(.*)', admin.site.root),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^smedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root':  settings.MEDIA_ROOT}),
  )
