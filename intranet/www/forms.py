#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.conf import settings
from django.utils.translation import ugettext as _

from intranet.org.models import Place


class EmailForm(forms.Form):
    email = forms.EmailField()


# http://plugins.jquery.com/project/datetime
class EventContactForm(forms.Form):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.8/jquery-ui.min.js',
            settings.MEDIA_URL + 'js/jquery.ui.datetime.min.js',
        )
        css = {'all': (
            settings.MEDIA_URL + 'css/jquery.ui.all.css',
            settings.MEDIA_URL + 'css/jquery.ui.datetime.css',
        )}

    facility = forms.ModelChoiceField(label=_(u'Prostor'), queryset=Place.objects.all())
    start_time = forms.DateTimeField(label=_(u'Začetek dogodka'),
        widget=widgets.DateTimeInput(attrs={'class': 'datetime-ui'}))
    end_time = forms.DateTimeField(label=_(u'Konec dogodka'),
        widget=widgets.DateTimeInput(attrs={'class': 'datetime-ui'}))
    text = forms.CharField(label=_(u'Opis dogodka'), widget=widgets.Textarea)
    contact = forms.EmailField(label=_(u'Kontaktna oseba (email)'))
