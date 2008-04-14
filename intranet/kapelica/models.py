from django.db import models
from django.contrib.auth.models import User
#from intranet.mediarchive import File
from django.core import validators
from datetime import date, time, timedelta
from intranet.org.models import Tag, Category, Place

# Create your models here.

class LocalCategory(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    cv = models.TextField(blank=True, null=True)

    class Admin:
        pass

    def __str__(self):
        return "%s %s" % (self.name, self.surname)

# koledar dogodkov
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateField(blank=True, null=True)
    artist = models.ManyToManyField(Artist,blank=True, null=True)
    local_category = models.ManyToManyField(LocalCategory)
    announce = models.TextField(blank=True, null=True)
#    media = models.ManyToManyField(File, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    place = models.ForeignKey(Place, related_name="kapelica_place")
    category = models.ManyToManyField(Category, related_name="kapelica_category")
    tags = models.ManyToManyField(Tag, blank=True, null=True, related_name="kapelica_tags")

    class Meta:
        verbose_name = 'Dogodek'
        verbose_name_plural = 'Dogodki'

    class Admin:
        search_fields = ['note','title']
        date_hierarchy = 'start_date'
        ordering = ['-end_date']
        list_filter = ['start_date']
        list_display = ['title', 'start_date']
        js = (
              'js/tags.js',
              )

    def __str__(self):
        return self.title

class General(models.Model):
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField()

    class Admin:
        pass

    def __str__(self):
        return self.title

class Link(models.Model):
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=50, blank=True, null=True)
    url = models.URLField()

    class Admin:
        pass

    def __str__(self):
        return self.title

