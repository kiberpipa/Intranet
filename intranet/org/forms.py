# coding=utf-8

import datetime
import time

from django import forms
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.conf import settings
from django import forms
from django.forms.util import ErrorList
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField

from intranet.org.models import TipSodelovanja, Person, Event, Sodelovanje
from intranet.org.models import Bug, Resolution, Clipping, Project, Alumni
from intranet.org.models import Category, UserProfile, Lend, Diary, Shopping
#from intranet.photologue.models import GalleryUpload

# DATETIMEWIDGET
calbtn = u"""<img src="http://www.up-rs.si/up-rs/uprs.nsf/calendar.jpg" alt="calendar" id="%s_btn" style="cursor: pointer; border: 1px solid #8888aa;" title="Select date and time"
            onmouseover="this.style.background='#444444';" onmouseout="this.style.background=''" />
<script type="text/javascript">
    Calendar.setup({
        inputField     :    "%s",
        ifFormat       :    "%s",
        button         :    "%s_btn",
        singleClick    :    true,
        showsTime      :    true,
    });
</script>"""

class DateTimeWidget(forms.widgets.TextInput):
    dformat = '%Y-%m-%d %H:%M'
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '': 
            try:
                final_attrs['value'] = \
                                   force_unicode(value.strftime(self.dformat))
            except:
                final_attrs['value'] = \
                                   force_unicode(value)
        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']
        
        jsdformat = self.dformat #.replace('%', '%%')
        cal = calbtn % (id, id, jsdformat, id)
        a = u'<input%s />%s' % (forms.util.flatatt(final_attrs), cal)
        return a

    def value_from_datadict(self, data, files, name):
        dtf = forms.fields.DEFAULT_DATETIME_INPUT_FORMATS
        empty_values = forms.fields.EMPTY_VALUES

        value = data.get(name, None)
        if value in empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime(value.year, value.month, value.day)
        for format in dtf:
            try:
                return datetime.datetime(*(time.strptime(value, format))[:6])
            except ValueError:
                continue
        return None

class EventFilter(forms.Form):
    title = forms.CharField(required=False)
    project = forms.ModelChoiceField(Project.objects.all().order_by('name'), required=False)
    category = forms.ModelChoiceField(Category.objects.all().order_by('name'), required=False)

class FilterBug(forms.Form):
    resolution = forms.ModelChoiceField(Resolution.objects.all(), required=False)
    assign = forms.ModelChoiceField(User.objects.filter(is_active=True).order_by('username'), required=False)
    author = forms.ModelChoiceField(User.objects.filter(is_active=True).order_by('username'), required=False)

    due_by = forms.DateTimeField(required=False)

    name = forms.CharField(required=False)


class CommentBug(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class DiaryFilter(forms.Form):
    task = forms.ModelChoiceField(Project.objects.all().order_by('name'), required=False)
    author = forms.ModelChoiceField(User.objects.filter(is_active=True).order_by('username'), required=False)

class ImenikFilter(forms.Form):
    project = forms.ModelChoiceField(Project.objects.all().order_by('name'), required=False)

class PersonForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=200, required=False)
    organization = forms.CharField(max_length=200, required=False)
    title = forms.CharField(max_length=200, required=False)

class ChangePw(forms.Form):
    oldpass = forms.CharField(max_length='200', widget=forms.PasswordInput)
    newpass1 = forms.CharField(max_length='200', widget=forms.PasswordInput)
    newpass2 = forms.CharField(max_length='200', widget=forms.PasswordInput)

class AddEventEmails(forms.Form):
    emails = forms.CharField(widget=forms.Textarea)

class EventForm(forms.ModelForm):
    resize = forms.CharField(widget=forms.HiddenInput, required=False)
    filename = forms.CharField(widget=forms.HiddenInput, required=False)
    start_date = forms.DateTimeField(widget=DateTimeWidget)
    class Meta:
        model = Event
        exclude = ('sequence')

    def clean(self):
        cleaned_data = self.cleaned_data
        public = cleaned_data.get("public")
        if public:
            if not ( cleaned_data.get("image") or self.instance.sequence > 0 ):
                self._errors["image"] = ErrorList(['ako je event public mores uploadat slikco'])
            elif not cleaned_data.get("resize"):
                self._errors["image"] = ErrorList(['public eventom mores oznacit del ki naj bi se prikazau na indexu (kliki na uploadano slikco)'])

            if not cleaned_data.get("announce"):
                self._errors["announce"] = ErrorList(['ako je event public mores napisat najavo'])
        
        return cleaned_data

class BugForm(forms.ModelForm):
    assign = ModelMultipleChoiceField(User.objects.exclude(first_name='').order_by('first_name'))
    assign.widget.attrs['size'] = 5
    assign.label_from_instance = lambda user: u"%s %s (%s)" % (user.first_name, user.last_name, user.username)

    watchers = ModelMultipleChoiceField(User.objects.exclude(first_name='').order_by('first_name'))
    watchers.widget.attrs['size'] = 5
    watchers.label_from_instance = lambda user: u"%s %s (%s)" % (user.first_name, user.last_name, user.username)
    watchers.help_text = u'<p class="notice"><small>Držite "CTRL" (ali "CMD" na Mac-u) za izbiro več kot enega.</small></p>'

    project = ModelMultipleChoiceField(Project.objects.all().order_by('name'))
    project.widget.attrs['size'] = 5

    class Meta:
        exclude = ('resolved', 'tags', 'author','parent',)
        model = Bug

class SodelovanjeFilter(forms.ModelForm):
    ##override the person in 'Sodelovanje', as there is required
    person = forms.ModelChoiceField(Person.objects.all(), required=False)
    c = [('', '---------'), ('txt', 'txt'), ('pdf', 'pdf'), ('csv', 'csv')]
    export = forms.ChoiceField(choices=c, required=False)

    class Meta:
        model = Sodelovanje
        exclude = ('note',)

class ClippingFilter(forms.ModelForm):
    c = [('', '---------'), ('xls', 'xls')]
    export = forms.ChoiceField(choices=c, required=False)
    class Meta:
        model = Clipping
        exclude = ('upload', 'deadline', 'feedback',)

class ClippingAdd(forms.ModelForm):
    class Meta:
        model = Clipping
        fields = ('name', 'article_name', 'medij', 'date')

class PipecForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = UserProfile
        exclude = ('user',)

class LendForm(forms.ModelForm):
    class Meta:
        model = Lend
        fields = ('what','to_who', 'from_who', 'contact_info', 'due_date',)

class ShoppingForm(forms.ModelForm):
    class Meta:
        model = Shopping
        fields = ('name', 'explanation', 'cost', 'project', )

class DiaryForm(forms.ModelForm):
    task = ModelChoiceField(Project.objects.all().order_by('name'))

    class Meta:
        model = Diary
        fields = ('task', 'date', 'length', 'log_formal', 'log_informal',)

class AlumniForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Alumni
        exclude = ('user',)
