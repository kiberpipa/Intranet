# coding=utf-8

import datetime
import re
import time

from django import forms
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.conf import settings
from django.forms.util import ErrorList
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField

from intranet.org.models import (TipSodelovanja, Person, Event, Sodelovanje,
    Project, Category, Lend, Diary, Shopping, IntranetImage, EmailBlacklist, User)

# DATETIMEWIDGET
# FUUUUUUUUcked up.
calbtn = u"""<img src="/smedia/img/calendar.jpg" alt="calendar" id="%s_btn" style="cursor: pointer; border: 1px solid #8888aa;" title="Select date and time"
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

class DiaryFilter(forms.Form):
    task = forms.ModelChoiceField(Project.objects.all().order_by('name'), required=False)
    author = forms.ModelChoiceField(User.objects.filter(is_active=True).order_by('username'), required=False)

class PersonForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=200, required=False)
    organization = forms.CharField(max_length=200, required=False)
    title = forms.CharField(max_length=200, required=False)

class AddEventEmails(forms.Form):
    emails = forms.CharField(widget=forms.Textarea(attrs={'cols':'31'}))

class CommaSeparatedIntegerField(forms.CharField):
    def clean(self, value):
        values = value.strip().split(',')
        for i in values:
            if not re.match('^\d+$', i):
                raise ValidationError("Integer is required.")
        return [int(i) for i in values]

class ImageResizeForm(forms.Form):
    resize = CommaSeparatedIntegerField(widget=forms.HiddenInput)
    filename = forms.CharField(widget=forms.HiddenInput)

class EmailBlacklistForm(forms.ModelForm):
    class Meta:
        model = EmailBlacklist

class IntranetImageForm(forms.ModelForm):
    class Meta:
        model = IntranetImage
        exclude = ('md5',)

class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(label="Čas pričetka", widget=DateTimeWidget)
    end_date = forms.DateTimeField(label="Zadnja ponovitev", widget=DateTimeWidget)
    title = forms.CharField(label="Naslov", max_length=Event._meta.get_field('title').max_length,
        widget=forms.TextInput(attrs={'size':'60'}))
    responsible = forms.CharField(label="Odgovorna oseba")
    #responsible = forms.ModelChoiceField(label="Odgovorna oseba", queryset=User.objects.filter(is_active=True).order_by('username'))

    class Meta:
        model = Event
        exclude = ('sequence', 'emails')

    def clean_responsible(self):
        resp = self.cleaned_data['responsible']
        try:
            return User.objects.filter(is_active=True).get(username=resp)
        except User.DoesNotExist:
            raise forms.ValidationError("Uporabnik ne obstaja")

    def clean(self):
        cleaned_data = self.cleaned_data
        public = cleaned_data.get("public")
        if public:
            if not ( cleaned_data.get("event_image") or self.instance.sequence > 0 ):
                self._errors["event_image"] = ErrorList(['Javni dogodki potrebujejo sliko.'])
            if not cleaned_data.get("announce"):
                self._errors["announce"] = ErrorList([u'Javni dogodki potrebujejo najavo.'])
        
        return cleaned_data

class SodelovanjeFilter(forms.ModelForm):
    ##override the person in 'Sodelovanje', as there is required
    person = forms.ModelChoiceField(Person.objects.all(), required=False)
    c = [('', '---------'), ('txt', 'txt'), ('pdf', 'pdf'), ('csv', 'csv')]
    export = forms.ChoiceField(choices=c, required=False)

    class Meta:
        model = Sodelovanje
        exclude = ('note',)

class LendForm(forms.ModelForm):
    from_who = ModelChoiceField(User.objects.filter(is_active=True).order_by('username'))

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

