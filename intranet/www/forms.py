#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField()
