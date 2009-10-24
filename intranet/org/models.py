from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

#from intranet.tags.models import Tag
#from intranet.tags import fields

from datetime import date, time, timedelta, datetime
import smtplib, string, audit
import socket
from PIL import Image
import re

# Create your models here.

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


#mercenaries

class SalaryType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class CostCenter(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Mercenary(models.Model):
    person = models.ForeignKey(User)
    amount = models.IntegerField()
    salary_type = models.ForeignKey(SalaryType)
    cost_center = models.ForeignKey(CostCenter)
    description = models.TextField()


    history = audit.AuditTrail()

    def __unicode__(self):
        return '%s: %s' % (self.person, self.amount)


class Project(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(User, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    salary_rate = models.FloatField(blank=True, null=True)
    verbose_name = models.CharField(max_length=255, blank=True, null=True)

    parent = models.ForeignKey('self', blank=True, null=True)
    history = audit.AuditTrail()

    salary_type = models.ForeignKey(SalaryType, blank=True, null=True)
    cost_center = models.ForeignKey(CostCenter, blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    
    #if True email all people which have this project set, if false email only Project.email
    # this needs null=True or else audit fails miserably
    email_members = models.NullBooleanField(default=True)

    #tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def children(self):
        related = []
        children = Project.objects.filter(parent = self)
        for child in children:
            second_level = Project.objects.filter(parent = child)

            if second_level:
                for s in child.children():
                    related.append(s)
            else:
                related.append(child)
        
        return related

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekti'

class UserProfile(models.Model):
    mobile = models.CharField(max_length=100)
    im = models.TextField(blank=True, null=True)
    #tags = models.ManyToManyField(Tag, blank=True, null=True)
    project = models.ManyToManyField(Project, blank=True, null=True)
    user = models.OneToOneField(User)
#    tasks = models.ManyToManyField(Task, blank=True, null=True)
#    project = models.ManyToManyField(Project, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    def is_active(self):
        whine = datetime.today() - timedelta(60)
        if Diary.objects.filter(author = self.user).filter(date__gt = whine):
            return True
        else:
            return False

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
         js = (
              'js/tags.js',
              )

class Place(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)

    #pub_date = models.DateTimeField(auto_now_add=True)
    #chg_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Admin:
         js = (
              'js/tags.js',
              )


##there's gotta be a better way to do this
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



# koledar dogodkov
class Event(models.Model):
    responsible = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    # XXX FIXME: unique is false on SlugField because of data inconsistancy
    slug = models.SlugField("event_slug",max_length=150, unique=False, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateField(blank=True, null=True)
    length = models.TimeField()
    project = models.ForeignKey(Project)
    technician = models.ManyToManyField(User,blank=True, null=True,verbose_name="Tehnik", related_name="event_technican")
    require_technician = models.BooleanField(default=False)
    require_video = models.BooleanField(default=False)
    visitors = models.IntegerField(default=0, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='events/%Y/%m/', verbose_name="Slikca za Event page")
    public = models.BooleanField(default=True)

    language = models.CharField(max_length=2, default='si', choices=settings.LANGUAGES, blank=True, null=True)

    #for iCal
    sequence = models.PositiveIntegerField(default=0)

    slides = models.FileField(upload_to='slides/%Y/%m/', blank=True, null=True)

    announce = models.TextField(blank=True, null=True)
    short_announce = models.TextField(blank=True, null= True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    place = models.ForeignKey(Place)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    #for video spamming
    emails = models.ManyToManyField(Email, blank=True, null=True)

    def index_image(self):
        index = re.sub('(?P<filename>.*)(?P<ext>\..*)', '\g<filename>-index\g<ext>', self.image._name)
        from os.path import exists
        if exists(settings.MEDIA_ROOT + index):
            return index
        else:
            return self.image._name

    def get_absolute_url(self):
        return '/intranet/events/%i/' %  self.id

    def get_public_url(self):
        return '/' + '/'.join(['event', self.start_date.strftime('%Y-%b-%d').lower(), unicode(self.id), self.slug]) + '/'

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        try:
            if Event.objects.get(pk=self.id).__dict__ != self.__dict__:
                self.sequence += 1
        except Event.DoesNotExist:
            pass
        super(Event, self).save()
        if self.image:
            filename = settings.MEDIA_ROOT + '/' + self.image._get_name()
            pic = Image.open(filename)
            width, height = pic.size
            width = float(width)
            height = float(height)
            q1 = width/400
            q2 = height/300
            if q1 > q2:
                q = q1
            else:
                q = q2

            if q > 1:
                new = pic.resize((int(width/q), int(height/q)))
                new.save(filename)

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


    class Meta:
        verbose_name = 'Dogodek'
        verbose_name_plural = 'Dogodki'

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

    def __unicode__(self):
        return self.name

class Sodelovanje(models.Model):
    event = models.ForeignKey(Event, blank=True, null=True)
    tip = models.ForeignKey(TipSodelovanja, blank=True, null=True)
    person = models.ForeignKey(Person)
    project = models.ForeignKey(Project, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s: %s @ %s" % (self.person, self.tip, self.event)
    
    def save(self):
        if self.event:
            self.project = self.event.project

        super(Sodelovanje, self).save()


##clipping
class Medij(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=40)

    def children(self):
        related = []
        children = Medij.objects.filter(parent = self)
        for child in children:
            second_level = Medij.objects.filter(parent = child)

            if second_level:
                for s in child.children():
                    related.append(s)
            else:
                related.append(child)
        
        return related
        

    def __unicode__(self):
        return self.name


class TipMedija(models.Model):
    name = models.CharField(max_length=40)


    def __unicode__(self):
        return self.name

class TipPrispevka(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Upload(models.Model):
    name = models.CharField(max_length=240)
    file = models.FileField(upload_to='clipping/')

    def __unicode__(self):  
        return self.name

class Clipping(models.Model):
    article_name = models.CharField(max_length=255, blank=True, null=True)
    medij = models.ForeignKey(Medij, blank=True, null=True)
    date = models.DateTimeField()
    

    event = models.ForeignKey(Event, blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    tip_medija = models.ForeignKey(TipMedija, blank=True, null=True)
    tip_prispevka = models.ForeignKey(TipPrispevka, blank=True, null=True)
    person = models.ForeignKey(Person, blank=True, null=True)
    rubrika = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    upload = models.ManyToManyField(Upload, blank=True, null=True)

    def __unicode__(self):
        return "%s, %s @ %s" % (self.tip_prispevka, self.medij, self.event)


# opravila v pipi
##XXX DEPRECIATED, use Project instead
class Task(models.Model):
    title = models.CharField(max_length=100)
    responsible = models.ForeignKey(User,blank=True, null=True)
    note = models.TextField(blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Opravilo'
        verbose_name_plural = 'Opravila'

    class Admin:
        search_fields = ['title','note']
        list_display = ['title', 'responsible']
        js = (
              'js/tags.js',
              )


# dnevnik dezurnih
class Diary(models.Model):
    author = models.ForeignKey(User, related_name="diary_author")
    task = models.ForeignKey(Project) #retained name for backwards compatibility
    date = models.DateTimeField(default=date.today())
    length = models.TimeField(default=time(4,0))
    event = models.ForeignKey(Event,blank=True, null=True)
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



# bugs
class Resolution(models.Model):
    name = models.CharField(max_length = 30)
    resolved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class StickyNote(models.Model):
    author = models.ForeignKey(User, related_name="message_author")
    post_date = models.DateField(default=date.today())
    due_date = models.DateField(default=(date.today() + timedelta(days=5)))
    note = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)


    def __unicode__ (self):
        return "%s..." % (self.note[:50])

    class Meta:
        verbose_name = 'Sporocilo'
        verbose_name_plural = 'Sporocila'

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

    def __unicode__ (self):
        return "%s (%s): %s" % (self.what, self.to_who, self.returned)

    def get_absolute_url(self):
        return '/intranet/lends/%d/' % self.id
        
    def days_due(self):
        return date.today() - self.due_date

    class Meta:
        verbose_name = 'Sposoja'
        verbose_name_plural = 'Sposoja'

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
        return "/intranet/kb/%s/%s/" % self.category.slug, self.slug

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


class Alumni(models.Model):
    facebook = models.CharField(max_length=150, blank=True, null=True)
    twitter = models.CharField(max_length=150, blank=True, null=True)
    linkedin = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    mail = models.CharField(max_length=150, blank=True, null=True)
    jabber = models.CharField(max_length=150, blank=True, null=True)
    msn = models.CharField(max_length=150, blank=True, null=True)
    yahoo = models.CharField(max_length=150, blank=True, null=True)
    skype = models.CharField(max_length=150, blank=True, null=True)
    www = models.CharField(max_length=150, blank=True, null=True)
    blog = models.CharField(max_length=150, blank=True, null=True)
    flickr = models.CharField(max_length=150, blank=True, null=True)

    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    image = models.ImageField(upload_to='alumni/', blank=True, null=True)

    def __unicode__(self):
        if self.user:
            return unicode(self.user)
        else:
            return self.text


