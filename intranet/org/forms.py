from django import forms
from django.contrib.auth.models import User

from intranet.org.models import TipSodelovanja, Person, Event, Sodelovanje
from intranet.org.models import Bug, Resolution, Clipping, Task, Project
from intranet.org.models import Category



class EventForm(forms.ModelForm):
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
    task = forms.ModelChoiceField(Task.objects.all(), required=False)
    author = forms.ModelChoiceField(User.objects.all(), required=False)


class ClippingFilter(forms.ModelForm):
    class Meta:
        model = Clipping

class ImenikFilter(forms.Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False)


class PersonForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=200, required=False)
    organization = forms.CharField(max_length=200, required=False)
    title = forms.CharField(max_length=200, required=False)

