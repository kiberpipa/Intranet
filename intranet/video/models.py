from django.db import models
from intranet.thumbnail.field import ImageWithThumbnailField

from intranet.org.models import Tag

class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, prepopulate_from=("name",))
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="video/category/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    pub_date = models.DateField(auto_now_add=True)
    chg_date = models.DateField(auto_now=True)

    class Admin:
        search_fields = ['name','description']
        list_display = ['name',]

    def __str__(self):
        return self.name

class Video(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, prepopulate_from=("name",), verbose_name="Kratko ime za URL")
    videocategory = models.ForeignKey(VideoCategory)
    baseurl = models.URLField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="video/images/", blank=True, null=True)
    featuring = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    length = models.TimeField()
    filesize = models.IntegerField(max_length=20, blank=True, null=True, verbose_name="File size in bytes")
    
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    pub_date = models.DateField(auto_now_add=True)
    chg_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Admin:
        search_fields = ['name','description','featuring']
        date_hierarchy = 'date'
        ordering = ['-date']
        list_filter = ['videocategory']
        list_display = ['name', 'featuring', 'date', 'length']
