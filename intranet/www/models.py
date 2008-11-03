from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from intranet.org.models import Event

# Create your models here.

#blog posts
class News(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150, unique=True)
    author = models.ForeignKey(User)
    #the field for calendar id's which can not be matched by  title to stories
    calendar_id = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('intranet.www.views.news', args=[self.slug])

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
    videodir = models.CharField(max_length=100)
    image_url = models.CharField(max_length=240)
    play_url = models.CharField(max_length=240)
    pub_date = models.DateTimeField()

    def __unicode__(self):
        return self.videodir
