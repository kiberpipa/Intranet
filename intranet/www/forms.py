#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.conf import settings
from django.utils.translation import ugettext as _

from intranet.org.models import Place
from intranet.www.models import News

from tinymce.widgets import TinyMCE

class EmailForm(forms.Form):
    email = forms.EmailField()


# http://plugins.jquery.com/project/datetime
class EventContactForm(forms.Form):
    # TODO: upgrade jquery and use internal
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.8/jquery-ui.min.js',
            settings.STATIC_URL + 'www/js/jquery.ui.datetime.min.js',
        )
        css = {'all': (
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/ui-darkness/jquery-ui.css',
            settings.STATIC_URL + 'www/css/jquery.ui.datetime.css',
        )}

    facility = forms.ModelChoiceField(label=_(u'Space'),
        queryset=Place.objects.filter(is_public=True),
        )
    start_time = forms.DateTimeField(label=_(u'Event start'),
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=widgets.DateTimeInput(attrs={'class': 'datetime-ui'}))
    end_time = forms.DateTimeField(label=_(u'Event end'),
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=widgets.DateTimeInput(attrs={'class': 'datetime-ui'}))
    text = forms.CharField(label=_(u'Event description'), widget=widgets.Textarea)
    contact = forms.EmailField(label=_(u'Contact person (email)'))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'image', 'text', 'language', 'author']
        widgets = {
            'text' : TinyMCE(mce_attrs={'height': 300}), # make it higher
        }
            