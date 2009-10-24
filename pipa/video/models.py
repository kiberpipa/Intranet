from django.db import models

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

