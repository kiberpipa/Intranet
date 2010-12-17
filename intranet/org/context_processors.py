#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


def django_settings(request):
    return {'settings': settings}

# TODO: DEPRECATE THOSE TWO
def media_url(request):
    return {
        'media_url': settings.MEDIA_URL,
    }

def admin_media_prefix(request):
    return {
        'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
    }
