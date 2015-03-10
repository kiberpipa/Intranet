#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.contrib.sites.models import Site
from django.core.urlresolvers import set_script_prefix
from django.core.urlresolvers import clear_script_prefix

from intranet.org.models import Scratchpad, Diary, Lend, Event


class Command(BaseCommand):
    args = "<date> in format dd.mm.yyyy"
    help = "Sends daily email repot about intranet changes"

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        if args:
            interested_datetime = datetime.datetime.strptime(args[0], '%d.%m.%Y')
        else:
            # yesterday
            interested_datetime = datetime.date.today() - datetime.timedelta(1)
        subject = 'Kiberpipa, dnevno porocilo: %d. %d. %d' % (interested_datetime.day, interested_datetime.month, interested_datetime.year)

        diaries = Diary.objects.filter(pub_date__year=interested_datetime.year, pub_date__month=interested_datetime.month, pub_date__day=interested_datetime.day)
        try:
            scratchpad = Scratchpad.objects.all()[0].content
        except Scratchpad.DoesNotExist:
            pass
        lends = Lend.objects.filter(returned=False)

        # warnings for events:
        # today and tomorrow
        events = Event.objects.get_date_events(
                                               datetime.datetime(interested_datetime.year, interested_datetime.month, interested_datetime.day, 0, 0) + relativedelta(days=1),
                                               datetime.datetime(interested_datetime.year, interested_datetime.month, interested_datetime.day, 0, 0) + relativedelta(days=3),
                                               )
        # no technician
        no_tech = events.filter(require_technician__exact=True).filter(technician__isnull=True)
        # no officers on duty
        no_responsible = events.filter(require_officers_on_duty__exact=True).filter(officers_on_duty__isnull=True)

        if diaries or no_tech or no_responsible:
            pass
        else:
            if self.verbosity >= 1:
                print "nothing to send"
            return

        # this causes url handling to force absolute urls
        url = "https://%s/" % Site.objects.get_current().domain
        set_script_prefix(url)

        try:
            text = get_template('mail/diary_report.txt').render(Context(locals()))
            html = get_template('mail/diary_report.html').render(Context(locals()))

            email = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, ['pipa-org@list.sou-lj.si'])
            email.attach_alternative(html, 'text/html')
            email.send()
            if self.verbosity >= 1:
                print "email sent"
        finally:
            # set_script_prefix is global for current thread
            clear_script_prefix()
