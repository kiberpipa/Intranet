from django.conf import settings
from django.conf.urls.defaults import *
from models import *

# Number of random images from the gallery to display.
SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', {'queryset': Gallery.objects.filter(parent__isnull = True), 'allow_empty': True}, name='pl-gallery-list'),
    url(r'^(?P<slug>[-\w\d]+)/$', 'object_detail', {'slug_field': 'title_slug', 'queryset': Gallery.objects.all()}, name='pl-gallery-detail'),
)

