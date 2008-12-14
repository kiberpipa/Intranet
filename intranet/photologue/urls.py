from django.conf import settings
from django.conf.urls.defaults import *
from models import *

# Number of random images from the gallery to display.
SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)

top = Gallery.objects.filter(parent__isnull=True)

print Gallery.objects.all()

def recurse(gallery):
    result = []
    result += [gallery]
    for i in Gallery.objects.filter(parent=gallery):
        if Gallery.objects.filter(parent=i):
            result += recurse(i)
        else:
            result += [i]
    return result

ordered = []
for g in top:
    ordered += recurse(g)


urlpatterns = patterns('django.views.generic.simple',
    (r'^', 'direct_to_template', {'template': 'photologue/gallery.html',
									'extra_context': {
									'ordered': ordered
									}}),
)

