# coding=utf-8

import re
import httplib
import datetime
from datetime import date

from chosen.widgets import ChosenSelectMultiple, ChosenSelect
from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils.formats import get_format
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE

from intranet.org.models import (Event, Project, Lend,
                                 Diary, Shopping, IntranetImage)

# TODO: i18n for widget
# TODO: obey settings.DATETIME_FORMAT
# TODO: document jquery ui css font-size change
# TODO: problem using existing datetime: https://github.com/trentrichardson/jQuery-Timepicker-Addon/issues/197


PYTHON_TO_JQUERY_DATETIME_FORMAT = {
        '%d': 'dd',
        '%m': 'mm',
        '%Y': 'yy',
        '%M': 'mm',
        '%H': 'hh',
        '%S': 'ss',
        #'%': '',
}


class SelectWidget(forms.widgets.Select):
    def render(self, name, value, attrs=None, choices=()):
        wattrs = attrs or dict()
        wattrs['class'] = "chzn-select"
        return forms.widgets.Select.render(self, name, value, attrs=wattrs, choices=choices)


class DateTimeWidget(forms.widgets.TextInput):
    """Datetimepicker implementation for Django.

    Dependencies: jquery, jquery.ui, slider
    URL: https://github.com/trentrichardson/jQuery-Timepicker-Addon

    """

    separator = " "
    date_format = "%Y/%m/%d"
    time_format = "%H:%M"
    class_ = 'jquery-timepicker'
    template = """
<script type="text/javascript">
    $('.%s').datetimepicker({
        dateFormat: '%s',
        timeFormat: '%s',
        stepHour: 1,
        stepMinute: 1,
        showButtonPanel: false,
        %s
    })
</script>
"""

    def __init__(self, *a, **kw):
        self.extra = kw.pop('extra', '')
        super(DateTimeWidget, self).__init__(*a, **kw)

    @property
    def format(self):
        return self.separator.join([self.date_format, self.time_format])

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}

        try:
            value = value.strftime(self.format)
        except:
            pass

        if 'class' in attrs:
            attrs['class'] += ' %s' % self.class_
        else:
            attrs.update({'class': self.class_})

        # convert python datetime format to jquerys
        for k, v in PYTHON_TO_JQUERY_DATETIME_FORMAT.iteritems():
            self.date_format = self.date_format.replace(k, v)
            self.time_format = self.time_format.replace(k, v)

        # render widget
        return super(DateTimeWidget, self).render(name, value, attrs) + self.template % (self.class_, self.date_format, self.time_format, self.extra)

    def value_from_datadict(self, data, files, name):
        value = super(DateTimeWidget, self).value_from_datadict(data, files, name)

        if isinstance(value, datetime.datetime):
            return value

        for fmt in [self.format] + list(get_format('DATETIME_INPUT_FORMATS')):
            try:
                return datetime.datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                pass


class DiaryFilter(forms.Form):
    task = forms.ModelChoiceField(label=_("Project"), queryset=Project.objects.all().order_by('name'), required=False)
    author = forms.ModelChoiceField(label=_("Author"), queryset=User.objects.filter(is_active=True).order_by('username'), required=False)


class AddEventEmails(forms.Form):
    emails = forms.CharField(widget=forms.Textarea(attrs={'cols': '31'}))


class CommaSeparatedIntegerField(forms.CharField):
    def clean(self, value):
        values = value.strip().split(',')
        for i in values:
            if not re.match('^\d+$', i):
                raise forms.ValidationError("Integer is required.")
        return [int(i) for i in values]


class ImageResizeForm(forms.Form):
    resize = CommaSeparatedIntegerField(widget=forms.HiddenInput)
    filename = forms.CharField(widget=forms.HiddenInput)


class IntranetImageForm(forms.ModelForm):
    class Meta:
        model = IntranetImage
        exclude = ('md5',)


class EventForm(forms.ModelForm):
    title = forms.CharField(label="Naslov", max_length=Event._meta.get_field('title').max_length,
        widget=forms.TextInput(attrs={'size': '60'}))

    class Meta:
        model = Event
        exclude = ('sequence', 'emails')
        widgets = {
            'project': SelectWidget(),
            'place': SelectWidget(),
            'responsible': SelectWidget(),
            'category': SelectWidget(),
            'language': SelectWidget(),
            # TODO: breaks ajax image 'event_image': SelectWidget(),
            'start_date': DateTimeWidget(extra="""
                onClose: function(date, inst) {
                    if ($('#id_end_date').datepicker('getDate') == null) {
                        $('#id_end_date').datepicker('setDate', date);
                    }
                }
            """),
            'end_date': DateTimeWidget,
        }

    def __init__(self, *a, **kw):
        super(EventForm, self).__init__(*a, **kw)

    def clean_responsible(self):
        resp = self.cleaned_data['responsible']
        try:
            return User.objects.get(username=resp)
        except User.DoesNotExist:
            raise forms.ValidationError("Uporabnik ne obstaja")

    def clean_flickr_set_id(self):
        resp = self.cleaned_data['flickr_set_id']
        if resp:
            conn = httplib.HTTPConnection("www.flickr.com")
            conn.request("HEAD", "/photos/kiberpipa/sets/%s/" % resp)
            if conn.getresponse().status != 200:
                raise forms.ValidationError(u"Set z takšnim id-jem ne obstaja")
        return resp

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if  start_date and end_date and start_date >= end_date:
            self._errors["end_date"] = ErrorList(['Zaključek se lahko zgodi samo po začetku dogodka.'])

        if cleaned_data.get("public"):
            if not (cleaned_data.get("event_image") or self.instance.sequence > 0):
                self._errors["event_image"] = ErrorList(['Javni dogodki potrebujejo sliko.'])
            if not cleaned_data.get("announce"):
                self._errors["announce"] = ErrorList([u'Javni dogodki potrebujejo najavo.'])

        return cleaned_data


class LendForm(forms.ModelForm):
    class Meta:
        model = Lend
        fields = ('what', 'from_who', 'to_who', 'contact_info', 'due_date',)
        widgets = {
            'from_who': ChosenSelect(overlay=u''),
        }

    def __init__(self, *a, **kw):
        super(LendForm, self).__init__(*a, **kw)
        self.fields['from_who'].queryset = User.objects.filter(is_active=True).order_by('username')


class ShoppingForm(forms.ModelForm):
    class Meta:
        model = Shopping
        fields = ('name', 'explanation', 'cost', 'project')
        widgets = {
            'project': ChosenSelectMultiple(overlay=u'Zberi enega ali več'),
        }

    def __init__(self, *a, **kw):
        # TODO: remove after this is applied: https://code.djangoproject.com/ticket/9321
        super(ShoppingForm, self).__init__(*a, **kw)
        self.fields['project'].help_text = ''


DIARY_BUTTONS = 'bold,italic,underline,strikethrough,separator,bullist,numlist,separator,link,image,separator,fullscreen'


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('task', 'event', 'date', 'length', 'log_formal', 'log_informal')
        widgets = {
            'date': DateTimeWidget,
            'event': SelectWidget(),
            'task': SelectWidget(),
            'log_formal': TinyMCE(mce_attrs={'theme_advanced_buttons1': DIARY_BUTTONS}),
            'log_informal': TinyMCE(mce_attrs={'theme_advanced_buttons1': DIARY_BUTTONS}),
        }

    def __init__(self, *a, **kw):
        self.base_fields['date'].initial = date.today()
        super(DiaryForm, self).__init__(*a, **kw)
        self.fields['task'].queryset = Project.objects.all().order_by('name')
        self.fields['event'].queryset = Event.objects.get_date_events(datetime.datetime.now() + datetime.timedelta(days=-21), datetime.datetime.now())
