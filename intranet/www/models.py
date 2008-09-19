from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150)

    def __unicode__(self):
        return self.title

class Ticker(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField()
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.name
