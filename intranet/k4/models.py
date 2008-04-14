from django.db import models
from intranet.org.models import Tag, Category, Place
from django.contrib.auth.models import User

# Create your models here.

# koledar dogodkov
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateField(blank=True, null=True)
    length = models.TimeField()

    announce = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    place = models.ForeignKey(Place, related_name="k4_place")
    category = models.ManyToManyField(Category, related_name="k4_category")
    tags = models.ManyToManyField(Tag, blank=True, null=True, related_name="k4_tags")

    class Meta:
        verbose_name = 'Dogodek'
        verbose_name_plural = 'Dogodki'

    class Admin:
        search_fields = ['note','title']
        date_hierarchy = 'start_date'
        ordering = ['-start_date']
        list_filter = [ 'start_date']
        list_display = ['title', 'start_date', 'length']

    def __str__(self):
        return self.title
