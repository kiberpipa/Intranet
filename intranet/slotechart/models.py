from django.db import models
from intranet.tags.models import Tag
from intranet.tags import fields

class Country(models.Model):
    name = models.CharField(maxlength=100)
    note = models.TextField(blank=True, null=True)

    class Admin:
        pass

    def __str__(self):
        return self.name

class Organisation(models.Model):
    name = models.CharField(maxlength=100)
    location = models.CharField(maxlength=100, blank=True, null=True)
    country = models.ForeignKey(Country)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Admin:
        pass

    def __str__(self):
        return "%s" % (self.name)

class Festival(models.Model):
    name = models.CharField(maxlength=100)
    location = models.CharField(maxlength=100, blank=True, null=True)
    country = models.ForeignKey(Country)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    producer = models.ManyToManyField(Organisation, related_name="festival_producer")
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __str__(self):
        return "%s" % (self.name)

class Award(models.Model):
    name = models.CharField(maxlength=100)
    festival = models.ManyToManyField(Festival, blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(maxlength=100)
    surname = models.CharField(maxlength=100)
    country = models.ForeignKey(Country)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    cv = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __str__(self):
        return "%s %s" % (self.name, self.surname)

class TechArtProject(models.Model):
    title = models.CharField(maxlength=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    collaborator = models.ManyToManyField(Artist,blank=True, null=True)
    artist = models.ManyToManyField(Artist,blank=True, null=True, related_name="sloartist")
    gallery_org = models.ManyToManyField(Organisation, blank=True, null=True)
    producer_org = models.ManyToManyField(Organisation, related_name="producer", blank=True, null=True)
    festival = models.ManyToManyField(Festival, blank=True, null=True)
    award = models.ManyToManyField(Award, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    tags = fields.TagsField(Tag, blank=True, null=True, related_name="project_tags")
    picture = models.URLField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __str__(self):
        return "%s" % (self.title)
