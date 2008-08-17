from django import forms
from django.contrib.auth.models import User

from intranet.org.models import TipSodelovanja, Person, Event, Sodelovanje
from intranet.org.models import Bug, Resolution, Clipping, Project
from intranet.org.models import Category

from django.utils.encoding import force_unicode
from django.conf import settings
from django import forms
import datetime
import time

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

class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=DateTimeWidget)
    class Meta:
        model = Event


class EventFilter(forms.Form):
    title = forms.CharField(required=False)
    project = forms.ModelChoiceField(Project.objects.all(), required=False)
    category = forms.ModelChoiceField(Category.objects.all(), required=False)

class FilterBug(forms.Form):
    resolution = forms.ModelChoiceField(Resolution.objects.all(), required=False)
    assign = forms.ModelChoiceField(User.objects.all(), required=False)
    author = forms.ModelChoiceField(User.objects.all(), required=False)

    due_by = forms.DateTimeField(required=False)

    name = forms.CharField(required=False)

class BugForm(forms.ModelForm):
    class Meta:
        exclude = ('resolved', 'tags', 'author',)
        model = Bug

class CommentBug(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class SodelovanjeFilter(forms.ModelForm):
    ##override the person in 'Sodelovanje', as there is required
    person = forms.ModelChoiceField(Person.objects.all(), required=False)
    c = [('', '---------'), ('txt', 'txt'), ('pdf', 'pdf'), ('csv', 'csv')]
    export = forms.ChoiceField(choices=c, required=False)

    class Meta:
        model = Sodelovanje
        exclude = ('note',)

class DiaryFilter(forms.Form):
    task = forms.ModelChoiceField(Project.objects.all(), required=False)
    author = forms.ModelChoiceField(User.objects.all(), required=False)


class ClippingFilter(forms.ModelForm):
    c = [('', '---------'), ('xls', 'xls')]
    export = forms.ChoiceField(choices=c, required=False)
    class Meta:
        model = Clipping
        exclude = ('upload', 'deadline', 'feedback',)

class ImenikFilter(forms.Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False)


class PersonForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=200, required=False)
    organization = forms.CharField(max_length=200, required=False)
    title = forms.CharField(max_length=200, required=False)

