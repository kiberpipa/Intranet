# *-* coding: utf-8 *-*

import time
import re
import urllib
import datetime
from hashlib import md5
from datetime import date, timedelta

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from pipa.mercenaries.models import CostCenter, SalaryType


def to_utc(dt):
    return time.gmtime(time.mktime(dt.timetuple()))


class Tag(models.Model):
    name = models.CharField(max_length=200, primary_key='True')
    total_ref = models.IntegerField(blank=True, default=0)
    font_size = models.IntegerField(blank=True, default=0)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/blog/tag/%s/" % (self.name)

    def __cmp__(self, other):
        return cmp(self.total_ref, other.total_ref)


class Project(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(User, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    salary_rate = models.FloatField(blank=True, null=True)
    verbose_name = models.CharField(max_length=255, blank=True, null=True)

    parent = models.ForeignKey('self', blank=True, null=True)

    salary_type = models.ForeignKey(SalaryType, blank=True, null=True)
    cost_center = models.ForeignKey(CostCenter, blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    #if True email all people which have this project set, if false email only Project.email
    # this needs null=True or else audit fails miserably
    email_members = models.NullBooleanField(default=True)

    #tags = models.ManyToManyField(Tag, blank=True, null=True)

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekti'
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def children(self):
        related = []
        children = Project.objects.filter(parent=self)
        for child in children:
            second_level = Project.objects.filter(parent=child)

            if second_level:
                for s in child.children():
                    related.append(s)
            else:
                related.append(child)
        return related


class Category(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)

    #tags = models.ManyToManyField(Tag, blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'm3c kategorija'
        verbose_name_plural = 'm3c kategorije'

    class Admin:
        js = ('js/tags.js',)


class Place(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Admin:
        js = ('js/tags.js',)


##there's gotta be a better way to do this
class EmailBlacklist(models.Model):
    blacklisted = models.EmailField(db_index=True, unique=True)

    def __unicode__(self):
        return self.email


class Email(models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return self.email


class Phone(models.Model):
    phone = models.CharField(max_length=100)

    def __unicode__(self):
        return self.phone


class Organization(models.Model):
    organization = models.CharField(max_length=100)

    def __unicode__(self):
        return self.organization


class Role(models.Model):
    role = models.CharField(max_length=100)

    def __unicode__(self):
        return self.role


class IntranetImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/%Y/%m/', verbose_name="Slikca za Event page")
    md5 = models.CharField(max_length=32, db_index=True, unique=True, blank=True)

    class Meta:
        ordering = ('-image',)

    def __unicode__(self):
        return u'Image: %s' % (self.image.url)

    def save(self, *args, **kwargs):
        super(IntranetImage, self).save(*args, **kwargs)
        self.md5 = md5(open(self.image.path).read()).hexdigest()
        super(IntranetImage, self).save(*args, **kwargs)


# koledar dogodkov
class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField("event_slug", max_length=150, unique=False, blank=True, null=True)

    require_technician = models.BooleanField(verbose_name="Dogodek potrebuje tehnika", default=False)
    require_video = models.BooleanField(verbose_name="Dogodek bo sneman", default=False)
    require_photo = models.BooleanField(verbose_name="Dogodek bo poslikan", default=True)
    # TODO: migrate to is_public
    public = models.BooleanField(verbose_name="Dogodek je javen", default=True)

    visitors = models.IntegerField(default=0, verbose_name=u"Številko obiskovalcev", blank=True, null=True)
    language = models.CharField(verbose_name="Jezik", max_length=2, default='sl', choices=settings.LANGUAGES, blank=True, null=True)
    #for iCal
    sequence = models.PositiveIntegerField(default=0)

    slides = models.FileField(upload_to='slides/%Y/%m/', verbose_name="Prosojnice", blank=True, null=True)

    announce = models.TextField(verbose_name="Uradna najava", blank=True, null=True)
    note = models.TextField(verbose_name="Opombe", blank=True, null=True)

    # time fields
    start_date = models.DateTimeField(verbose_name=u"Pričetek", db_index=True)
    end_date = models.DateTimeField(verbose_name=u"Zaključek", blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    # relations
    responsible = models.ForeignKey(User, verbose_name="Odgovorna oseba")
    place = models.ForeignKey(Place, verbose_name="Prostor")
    category = models.ForeignKey(Category, verbose_name="Kategorija")
    project = models.ForeignKey(Project, verbose_name="V okviru projekta")
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    technician = models.ManyToManyField(User, verbose_name="Tehnik", blank=True, null=True, related_name="event_technican")

    # flickr set id
    # TODO: refactor in new app
    flickr_set_id = models.BigIntegerField(verbose_name="Flickr set ID", blank=True, null=True)

    # for video spamming
    emails = models.ManyToManyField(Email, blank=True, null=True)
    event_image = models.ForeignKey(IntranetImage, verbose_name="Slika", null=True, blank=True)

    class Meta:
        verbose_name = 'Dogodek'
        verbose_name_plural = 'Dogodki'
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/intranet/events/%i/' % self.id

    def get_public_url(self):
        return reverse('event_detail', kwargs=dict(id=self.id, slug=self.slug))

    @property
    def length(self):
        return (self.end_date - self.start_date).seconds / 3600.0

    def save(self):
        self.slug = slugify(self.title)
        try:
            if Event.objects.get(pk=self.id).__dict__ != self.__dict__:
                self.sequence += 1
        except Event.DoesNotExist:
            pass
        super(Event, self).save()

    def index_image(self):
        index = re.sub('(?P<filename>.*)(?P<ext>\..*)', '\g<filename>-index\g<ext>', self.image._name)
        from os.path import exists
        if exists(settings.MEDIA_ROOT + index):
            return index
        else:
            return self.image._name

    def flickr_url(self):
        return 'http://www.flickr.com/photos/kiberpipa/sets/%s/' % self.flickr_set_id

    def google_calendar_url(self):
        data = [('action', 'TEMPLATE'),
            ('text', self.title.encode('utf-8')),
            ('dates', '%s/%s' % (time.strftime('%Y%m%dT%H%M%SZ', to_utc(self.start_date)), time.strftime('%Y%m%dT%H%M%SZ', to_utc(self.end_date)))),
            ('sprop', 'website:www.kiberpipa.org'),
            ('sprop', 'name:Kiberpipa - %s' % self.project.name.encode('utf-8')),
            # take first 24 words of announce
            ('details', (u' '.join(self.announce.split(u' ')[:24])).encode('utf-8')),
            ('location', '%s, Kiberpipa, Ljubljana' % self.place),
            ]
        qs = urllib.urlencode(data)
        return 'http://www.google.com/calendar/event?' + qs

    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_start_date' % direction)(public__exact=True)

    def get_next(self):
        """
        Returns the next Entry with "live" status by ``pub_date``, if
        there is one, or ``None`` if there isn't.

        In public-facing templates, use this method instead of
        ``get_next_by_pub_date``, because ``get_next_by_pub_date``
        does not differentiate entry status.

        """
        return self._next_previous_helper('next')

    def get_previous(self):
        """
        Returns the previous Entry with "live" status by ``pub_date``,
        if there is one, or ``None`` if there isn't.

        In public-facing templates, use this method instead of
        ``get_previous_by_pub_date``, because
        ``get_previous_by_pub_date`` does not differentiate entry
        status..

        """
        return self._next_previous_helper('previous')

    def get_video_url(self):
        from pipa.video.models import Video
        return Video.objects.get(event=self).play_url


class TipSodelovanja(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=230, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)

    email = models.ManyToManyField(Email, blank=True, null=True)
    phone = models.ManyToManyField(Phone, blank=True, null=True)
    organization = models.ManyToManyField(Organization, blank=True, null=True)
    role = models.ManyToManyField(Role, blank=True, null=True)

    #najbrz bi blo pametno met poljubno stevilo teh stvari
    #phone = models.CharField(max_length=40)
    #mail = models.EmailField()
    #organization = models.CharField(max_length=100)

    #reseno z objektkom Sodelovanje
    #sodelovanje = models.ManyToManyField(Sodelovanje, blank=True, null=True)
    #- eventi
    #- tip sodelovanja (predavatelj, voditelj predavanja, sponzor .... )

    ##TODO
    #- projekti ##should be parsed from Event, i think
    #- `vloga' (a je tip/bejba novinar, direktor, marketingar...)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Sodelovanje(models.Model):
    event = models.ForeignKey(Event, blank=True, null=True)
    tip = models.ForeignKey(TipSodelovanja, blank=True, null=True)
    person = models.ForeignKey(Person)
    project = models.ForeignKey(Project, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-event__start_date',)

    def __unicode__(self):
        return u"%s: %s @ %s" % (self.person, self.tip, self.event)

    def save(self):
        if self.event:
            self.project = self.event.project

        super(Sodelovanje, self).save()


# opravila v pipi
##XXX DEPRECIATED, use Project instead
class Task(models.Model):
    title = models.CharField(max_length=100)
    responsible = models.ForeignKey(User, blank=True, null=True)
    note = models.TextField(blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Opravilo'
        verbose_name_plural = 'Opravila'

    class Admin:
        search_fields = ['title', 'note']
        list_display = ['title', 'responsible']
        js = ('js/tags.js',)


# dnevnik dezurnih
class Diary(models.Model):
    author = models.ForeignKey(User, related_name="diary_author")
    task = models.ForeignKey(Project)  # retained name for backwards compatibility
    date = models.DateTimeField(default=date.today(), db_index=True)
    length = models.TimeField(default=datetime.time(4, 0))
    event = models.ForeignKey(Event, blank=True, null=True)
    log_formal = models.TextField()
    log_informal = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __unicode__(self):
        #return "%s - %s: %s... (%s)" % (self.date.strftime('%x'), self.get_author(), self.log_formal[:66], self.length)
        return "%s" % self.log_formal

    def get_absolute_url(self):
        return "/intranet/diarys/%i/" % self.id

    class Meta:
        verbose_name = 'Dnevnik'
        verbose_name_plural = 'Dnevniki'


class StickyNote(models.Model):
    class Meta:
        verbose_name = 'Sporocilo'
        verbose_name_plural = 'Sporocila'

    author = models.ForeignKey(User, related_name="message_author")
    post_date = models.DateField(default=date.today())
    due_date = models.DateField(default=(date.today() + timedelta(days=5)))
    note = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __unicode__(self):
        return "%s..." % (self.note[:50])

    def get_absolute_url(self):
        return '/intranet/admin/org/stickynote/%d/' % self.id


class Lend(models.Model):
    what = models.CharField(max_length=200, verbose_name='Predmet')
    to_who = models.CharField(max_length=200, verbose_name='Komu', blank=True, null=True)
    from_who = models.ForeignKey(User, verbose_name='Odobril')
    from_date = models.DateField(default=date.today())
    due_date = models.DateField(default=(date.today() + timedelta(days=1)))
    contact_info = models.CharField(max_length=100, verbose_name='Kontakt', blank=True, null=True)
    why = models.CharField(max_length=200, verbose_name='Namen', blank=True, null=True)
    returned = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s (%s): %s" % (self.what, self.to_who, self.returned)

    def get_absolute_url(self):
        return '/intranet/lends/%d/' % self.id

    def days_due(self):
        return date.today() - self.due_date

    class Meta:
        verbose_name = 'Sposoja'
        verbose_name_plural = 'Sposoja'


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
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/intranet/shopping/%i/" % self.id


class Scratchpad(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Kracarka'
        verbose_name_plural = 'Kracarka'
