#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='announce/%Y/%m/', verbose_name="Slika ob objavi")
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    author = models.ForeignKey(User)
    #the field for calendar id's which can not be matched by title to stories
    calendar_id = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=2, default='si', choices=settings.LANGUAGES, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('intranet.www.views.news_detail', args=[self.id, self.slug])

    def __unicode__(self):
        return self.title
