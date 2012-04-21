#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _


class LDAPPasswordChangeForm(forms.Form):
    old_password = forms.CharField(max_length='200', widget=forms.PasswordInput)
    new_password = forms.CharField(max_length='200', widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(max_length='200', widget=forms.PasswordInput)


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label=_('Remember me'), required=False)
