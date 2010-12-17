from django.db import models
from intranet.org.models import Event

class Video(models.Model):
    #compatiblity layer with current video archive
    event = models.ForeignKey(Event, blank=True, null=True, related_name="video")
    #unique video identifier, requested by ike
    videodir = models.CharField(max_length=100, unique=True)
    image_url = models.CharField(max_length=240)
    play_url = models.CharField(max_length=240)
    pub_date = models.DateTimeField(db_index=True)

    def __unicode__(self):
        return self.videodir

    def get_absolute_url(self):
        return self.play_url
