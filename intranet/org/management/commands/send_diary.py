#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.contrib.sites.models import Site
from django.core.urlresolvers import set_script_prefix

from intranet.org.models import Scratchpad, Diary, Lend, Event


class Command(BaseCommand):
    args = "<date> in format dd.mm.yyyy"
    help = "Sends daily email repot about intranet changes"

    def handle(self, *args, **options):
        if args:
            now = datetime.datetime.strptime(args[0], '%d.%m.%Y')
        else:
            # yesterday
            now = datetime.date.today() - datetime.timedelta(1)
        subject = 'Kiberpipa, dnevno porocilo: %d. %d. %d' % (now.day, now.month, now.year)

        diaries = Diary.objects.filter(pub_date__year=now.year, pub_date__month=now.month, pub_date__day=now.day)
        try:
            scratchpad = Scratchpad.objects.all()[0].content
        except Scratchpad.DoesNotExist:
            pass
        lends =  Lend.objects.filter(returned=False)
        
        # warnings for events:
        # today and tomorrow
        events = Event.objects.filter(start_date__gt=datetime.datetime(now.year, now.month, now.day+1, 0, 0))
        events = events.filter(start_date__lt=datetime.datetime(now.year, now.month, now.day+3, 0, 0))
        # no technician
        no_tech = events.filter(require_technician__exact=True).filter(technician__isnull=True)
        # no responsible (for future compatibility)
        no_responsible = events.filter(responsible__isnull=True)

        if diaries or no_tech or no_responsible:
            pass
        else:
            print "nothing to send"
            return

        # this causes url handling to force absolute urls
        url = "https://%s/" % Site.objects.get_current().domain
        set_script_prefix(url)

        text = get_template('mail/diary_report.txt').render(Context(locals()))
        html = get_template('mail/diary_report.html').render(Context(locals()))

        email = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, ['pipa-org@list.sou-lj.si'])
        email.attach_alternative(html, 'text/html')
        email.send()
        print "email sent"
