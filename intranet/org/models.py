from django.db import models
from django.contrib.auth.models import User

#from intranet.tags.models import Tag
#from intranet.tags import fields

from django.core import validators
from datetime import date, time, timedelta

from django.conf import settings

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200, primary_key='True', core=True)
    total_ref = models.IntegerField(blank=True, default=0)
    font_size = models.IntegerField(blank=True, default=0)

    class Admin:
        pass

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/blog/tag/%s/" % (self.name)

    def __cmp__(self, other):
        return cmp(self.total_ref, other.total_ref)

class UserProfile(models.Model):
    mobile = models.CharField(max_length=100)
    im = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    user = models.OneToOneField(User)
#    tasks = models.ManyToManyField(Task, blank=True, null=True)
#    project = models.ManyToManyField(Project, blank=True, null=True)

    class Admin:
        pass

    def __unicode__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(User)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=True, null=True)

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekti'

    class Admin:
        search_fields = ['note','name','responsible']
        list_display = ['name', 'responsible']
        js = (
              'js/tags.js',
              )

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
         js = (
              'js/tags.js',
              )

    def __unicode__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
         js = (
              'js/tags.js',
              )

    def __unicode__(self):
        return self.name

class PlaceInternal(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(User)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
         js = (
              'js/tags.js',
              )

    def __unicode__(self):
        return self.name


# koledar dogodkov
class Event(models.Model):
    responsible = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateField(blank=True, null=True)
    length = models.TimeField()
    project = models.ForeignKey(Project)
    technician = models.ForeignKey(User,blank=True, null=True,verbose_name="Tehnik", related_name="event_technican")
    require_technician = models.BooleanField(default=False)
    require_video = models.BooleanField(default=False)
    visitors = models.IntegerField(default=0, blank=True, null=True)

    announce = models.TextField(blank=True, null=True)
    short_announce = models.TextField(blank=True, null= True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    place = models.ForeignKey(Place)
    place_internal = models.ManyToManyField(PlaceInternal)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    class Meta:
        verbose_name = 'Dogodek'
        verbose_name_plural = 'Dogodki'

    class Admin:
        search_fields = ['note','title','project', 'announce']
        date_hierarchy = 'start_date'
        ordering = ['-start_date']
        list_filter = ['project', 'start_date']
        list_display = ['title', 'start_date', 'length']
        js = (
              'js/tags.js',
              )

    def get_absolute_url(self):
        return "%s/intranet/events/%i/" % (settings.BASE_URL, self.id)

    def __unicode__(self):
        return self.title
        #return "%s - (%s) %s" % (self.date.strftime('%x'), self.get_project().name, self.title)

# opravila v pipi
class Task(models.Model):
    title = models.CharField(max_length=100)
    responsible = models.ForeignKey(User,blank=True, null=True)
    note = models.TextField(blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Opravilo'
        verbose_name_plural = 'Opravila'

    class Admin:
        search_fields = ['title','note']
        list_display = ['title', 'responsible']
        js = (
              'js/tags.js',
              )

    def __unicode__(self):
        return self.title

# dnevnik dezurnih
class Diary(models.Model):
    author = models.ForeignKey(User, related_name="diary_author")
    task = models.ForeignKey(Task)
    date = models.DateTimeField(default=date.today())
    length = models.TimeField(default=time(3,0))
    event = models.ForeignKey(Event,blank=True, null=True)
    log_formal = models.TextField()
    log_informal = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    class Meta:
        verbose_name = 'Dnevnik'
        verbose_name_plural = 'Dnevniki'

    class Admin:
        search_fields = ['log_formal','person','task']
        date_hierarchy = 'date'
        list_filter = ['date', 'task', 'author']
        list_display = ('date', 'author', 'task', 'length')
        js = (
              'js/tags.js',
              )

    def __unicode__(self):
        #return "%s - %s: %s... (%s)" % (self.date.strftime('%x'), self.get_author(), self.log_formal[:66], self.length)
        return "%s" % self.log_formal

    def get_absolute_url(self):
        return "%s/diarys/%i/" % (settings.BASE_URL, self.id)

# bugs
class Bug(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="bug_author")
    assign = models.ForeignKey(User,blank=True, null=True, related_name="bug_assign")
    resolved = models.BooleanField()
    note = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    class Meta:
        verbose_name = 'Hrosc'
        verbose_name_plural = 'Hrosci'

    class Admin:
        search_fields = ['note','name','assign']
        list_filter = ['resolved', 'assign']
        list_display = ['name', 'id', 'resolved', 'author', 'assign']
        ordering = ['resolved']

    def __unicode__(self):
      return self.name

    def get_absolute_url(self):
        return "%s/intranet/bugs/%i/" % (settings.BASE_URL, self.id)

class StickyNote(models.Model):
    author = models.ForeignKey(User, related_name="message_author")
    post_date = models.DateField(default=date.today())
    due_date = models.DateField(default=(date.today() + timedelta(days=5)))
    note = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)


    class Meta:
        verbose_name = 'Sporocilo'
        verbose_name_plural = 'Sporocila'

    class Admin:
        search_fields = ['note']
        date_hierarchy = 'due_date'
        list_filter = ['due_date', 'author']
        js = (
              'js/tags.js',
              )

    def __unicode__ (self):
        return "%s..." % (self.note[:50])

class Lend(models.Model):
    what = models.CharField(max_length=200, verbose_name='Predmet')
    to_who = models.CharField(max_length=200, verbose_name='Komu', blank=True, null=True)
    from_who = models.ForeignKey(User, verbose_name='Odobril')
    from_date = models.DateField(default=date.today())
    due_date = models.DateField(default=(date.today() + timedelta(days=1)))
    contact_info = models.CharField(max_length=100, verbose_name='Kontakt', blank=True, null=True)
    why = models.CharField(max_length=200, verbose_name='Namen')
    returned = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sposoja'
        verbose_name_plural = 'Sposoja'

    class Admin:
        search_fields = ['to_who', 'why', 'note']
        list_display = ['what', 'returned', 'from_who', 'to_who', 'from_date', 'due_date', 'why']

    def __unicode__ (self):
        return "%s (%s): %s" % (self.what, self.to_who, self.returned)


class KbCategory(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=75, )

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __unicode__(self):
        return self.title

class KB(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=75, )
    category = models.ForeignKey(KbCategory)
    project = models. ManyToManyField(Project, blank=True, null=True)
    task = models.ManyToManyField(Task, blank=True, null=True)
    content = models.TextField()
    editor = models.ForeignKey(User)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "%s/intranet/kb/%s/%s/" % (settings.BASE_URL, self.category.slug, self.slug)

class Shopping(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="shopping_author")
    explanation = models.TextField()
    cost = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    #amount = models.IntegerField(default=1)
    bought = models.BooleanField(default=False)

    supporters = models.ManyToManyField(User, blank=True, null=True, related_name="shopping_supporters")
    responsible = models.ForeignKey(User, blank=True, null=True, related_name="shopping_responsible")

    project = models.ManyToManyField(Project, blank=True, null=True)
    task = models.ManyToManyField(Task, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Admin:
        pass

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "%s/intranet/shopping/%i/" % (settings.BASE_URL, self.id)

class Scratchpad(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User)
  
    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    
    class Admin:
        pass
        
    class Meta:
        get_latest_by = "id"
    
