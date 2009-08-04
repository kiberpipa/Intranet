from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from intranet.org.models import Event
from photologue.models import Gallery as PGallery

# Create your models here.

#blog posts
class News(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='announce/%Y/%m/', verbose_name="Slika ob objavi")
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150, unique=True)
    author = models.ForeignKey(User)
    #the field for calendar id's which can not be matched by  title to stories
    calendar_id = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=2, default='si', choices=settings.LANGUAGES, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('intranet.www.views.news_detail', args=[self.slug])

    def __unicode__(self):
        return self.title

class Ticker(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField()
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.name

class Video(models.Model):
    #compatiblity layer with current video archive
    event = models.ForeignKey(Event, blank=True, null=True)
    #unique video identifier, requested by ike
    videodir = models.CharField(max_length=100, unique=True)
    image_url = models.CharField(max_length=240)
    play_url = models.CharField(max_length=240)
    pub_date = models.DateTimeField()

    def __unicode__(self):
        return self.videodir

class Gallery(PGallery):
    parent = models.ForeignKey('self', blank=True, null=True)
    event = models.ForeignKey(Event, blank=True, null=True)
    album_name= models.CharField(max_length=250)

    def sample(self):
        #import pdb; pdb.set_trace()
        import random
        #ups = [i.sample() for i in Gallery.objects.filter(parent=self)]
        ups = [i.sample() for i in self.gallery_set.all()] + PGallery.sample(self)
        random.shuffle(ups)
        if ups:
            return ups[0]
        else:
            return None
