#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import set_script_prefix
from django.core.urlresolvers import clear_script_prefix
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import Context
from django.template.loader import get_template
from django.utils import translation

from intranet.org.models import Event


class Command(BaseCommand):
    args = "<date> in format dd.mm.yyyy"
    help = "Sends weekly email repot about events"

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))

        # commands need explicit activation of translations
        translation.activate(settings.LANGUAGE_CODE)
        # this causes url handling to force absolute urls
        url = "https://%s/" % Site.objects.get_current().domain
        set_script_prefix(url)

        try:
            if args:
                now = datetime.datetime.strptime(args[0], '%d.%m.%Y')
            else:
                # yesterday
                now = datetime.date.today() - datetime.timedelta(1)

            subject = 'Kiberpipa, weekly report: %d. %d. %d' % (now.day, now.month, now.year)
            days_range = 7
            events = Event.objects.all()

            # 1. events that are newer or equal may pass
            # 2. events that are older or equal may pass
            events = events.filter(start_date__gte=(now - datetime.timedelta(days=days_range))).filter(start_date__lte=now)

            all_visitors = 0
            for e in events:
                all_visitors += e.visitors or 0

            # is public and no visitors
            no_visitors = events.filter(public__exact=True).filter(visitors__exact=0)

            # is videoed and no attached video
            no_video = events.filter(require_video__exact=True).filter(video__isnull=True)

            # is pictured and no flicker id
            no_pictures = events.filter(require_photo__exact=True).filter(flickr_set_id__exact=None)

            if events.count() == 0:
                if self.verbosity >= 1:
                    print "no events to send"
                return

            unfinished_events = (no_visitors, no_video, no_pictures)
            html = get_template('mail/events_report.html').render(Context({
                                                                  'days_range': days_range,
                                                                  'all_visitors': all_visitors,
                                                                  'events': events,
                                                                  'unfinished_events': unfinished_events
                                                                  }))
            text = get_template('mail/events_report.txt').render(Context({
                                                                  'days_range': days_range,
                                                                  'all_visitors': all_visitors,
                                                                  'events': events,
                                                                  'unfinished_events': unfinished_events
                                                                  }))

            email = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, ['pipa-org@list.sou-lj.si'])
            email.attach_alternative(html, 'text/html')
            email.send()
            if self.verbosity >= 1:
                print "events email sent"
        finally:
            # set_script_prefix is global for current thread
            clear_script_prefix()
