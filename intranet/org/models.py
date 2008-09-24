from django.db import models
from django.contrib.auth.models import User

#from intranet.tags.models import Tag
#from intranet.tags import fields

from django.core import validators
from datetime import date, time, timedelta, datetime
import smtplib, string, audit

from django.conf import settings

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


    history = audit.AuditTrail()

    def __unicode__(self):
        return '%s: %s' % (self.person, self.amount)


class Project(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(User, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    salary_rate = models.FloatField(blank=True, null=True)

    parent = models.ForeignKey('self', blank=True, null=True)
    history = audit.AuditTrail()

    salary_type = models.ForeignKey(SalaryType, blank=True, null=True)
    cost_center = models.ForeignKey(CostCenter, blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

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

# koledar dogodkov
class Event(models.Model):
    responsible = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    slug = models.SlugField("event_slug",max_length=150,unique=True, blank=True, null=True)
    #author = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateField(blank=True, null=True)
    length = models.TimeField()
    project = models.ForeignKey(Project)
    technician = models.ForeignKey(User,blank=True, null=True,verbose_name="Tehnik", related_name="event_technican")
    require_technician = models.BooleanField(default=False)
    require_video = models.BooleanField(default=False)
    visitors = models.IntegerField(default=0, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='events/%Y/%m/')

    slides = models.FileField(upload_to='slides/%Y/%m/', blank=True, null=True)

    announce = models.TextField(blank=True, null=True)
    short_announce = models.TextField(blank=True, null= True)
    note = models.TextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)

    place = models.ForeignKey(Place)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True, null=True)


    def get_absolute_url(self):
        return "%s/intranet/events/%i/" % (settings.BASE_URL, self.id)

    def __unicode__(self):
        return self.title


    class Meta:
        verbose_name = 'Dogodek'
        verbose_name_plural = 'Dogodki'

class TipSodelovanja(models.Model):
    name = models.CharField(max_length=40)


    def __unicode__(self):
        return self.name


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
        return "%s: %s @ %s" % (self.person, self.tip, self.event)
    
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
    event = models.ForeignKey(Event, blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    tip_medija = models.ForeignKey(TipMedija, blank=True, null=True)
    medij = models.ForeignKey(Medij, blank=True, null=True)
    tip_prispevka = models.ForeignKey(TipPrispevka, blank=True, null=True)
    person = models.ForeignKey(Person)
    rubrika = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    deadline = models.CharField(max_length=255)
    feedback = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

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
        return "%s/diarys/%i/" % (settings.BASE_URL, self.id)

    class Meta:
        verbose_name = 'Dnevnik'
        verbose_name_plural = 'Dnevniki'



# bugs
class Resolution(models.Model):
    name = models.CharField(max_length = 30)

    def __unicode__(self):
        return self.name

class Bug(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="bug_author")
    #assign = models.ForeignKey(User,blank=True, null=True, related_name="bug_assign")
    assign = models.ManyToManyField(User,blank=True, null=True, related_name="bug_assign")
    project = models.ManyToManyField(Project, blank=True, null=True)
    resolved = models.BooleanField()
    resolution = models.ForeignKey(Resolution, blank = True, null = True)
    note = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True)
    due_by = models.DateTimeField(null=True, blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __unicode__(self):
      return self.name

    def get_absolute_url(self):
        return "%s/intranet/bugs/%i/" % (settings.BASE_URL, self.id)
    
    def mail(self, message='', subject='you have new bug'):

        ##the stuff we'll need to send mail
        mail_from = 'intranet@kiberpipa.org'

        ##get  a string of all assignees
        assignees = ''
        for assignee in self.assign.all():
            assignees += assignee.__unicode__()

        projects = ''
        for project in self.project.all():
            projects += project.__unicode__()

        info = 'bug: #%i\n' % self.id
        info += 'bug url: %s\n' % self.get_absolute_url()
        if assignees:
            info += 'assigned to: %s\n' % assignees
        if projects:
            info += 'assigned to (projects): %s\n' % projects
        info += 'reported by: %s\n' % self.author
        if self.due_by:
            info += 'DEADLINE: %s\n' % self.due_by

        ##separator
        if message:
            info += '-------------------------------------\n\n\n'

        #construct a list of all mails to which to compailn
        mails = []
        for i in self.assign.all():
            if i.email not in mails and i.email:
             mails += [i.email]

        for i in Comment.objects.filter(bug=self):
            if not i.author.email in mails and i.author.email:
                mails += [i.author.email]

        if self.author.email not in mails and self.author.email:
            mails += [self.author.email]

        for i in self.project.all():
            if not i.email in mails and i.email:
                mails += [i.email]

        #send the mail to all the assignees
        for to in mails:
            msg = "From: %s\nTo: %s\nSubject: %s\n\n%s\n%s"  % (mail_from, to, subject, info, message)

            session = smtplib.SMTP('localhost')
            session.sendmail(mail_from, to, msg)
            session.close()

    def get_related(self):
        #get parent and children bugs
        top = self
        while top.parent != None:
            top = top.parent

        children = top._children()
        children.remove(self)
        return children

    def _children(self):
        related = [self]
        children = Bug.objects.filter(parent = self)
        for child in children:
            second_level = Bug.objects.filter(parent = child)

            if second_level:
                for s in child._children():
                    related.append(s)
            else:
                related.append(child)
        
        return related


    def save(self):
    ##the one and only place where we shall decide how bug is considered open
#        id: 1, name: WONTFIX
#        id: 2, name: CANTFIX
#        id: 3, name: WORKSFORME
#        id: 4, name: INVALID
#        id: 5, name: FIXED
#        id: 6, name: OPEN
        #self.author = request.user

        if self.resolution == None:
            self.resolution = Resolution.objects.get(pk=6)

        if self.resolution.id <= 5:
            self.resolved = True;
        else:
            self.resolved = False
        super(Bug, self).save()

    class Meta:
        verbose_name = 'Hrosc'
        verbose_name_plural = 'Hrosci'


class Comment(models.Model):
    bug = models.ForeignKey(Bug)
    date = models.DateTimeField(auto_now = True)
    text = models.TextField()
    author = models.ForeignKey(User, related_name="comment_author")


    def save(self, request):
        self.author = request.user
        super(Comment, self).save()

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
        return '%s/intranet/lends/%d' % (settings.BASE_URL, self.id)

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

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "%s/intranet/shopping/%i/" % (settings.BASE_URL, self.id)

class Scratchpad(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User)
  
    pub_date = models.DateTimeField(auto_now_add=True)
    chg_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Kracarka'
        verbose_name_plural = 'Kracarka'
