# *-* coding: utf-8 *-*

import urllib
import re
import datetime
import time
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template import loader

from pipa.video.models import Video
from intranet.org.models import Event


TABINDEX_URL = 'http://video.kiberpipa.org/tabindex.txt'
INFOTXT_URL = 'http://video.kiberpipa.org/media/%s/info.txt'


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--notifications', action='store_true', dest='notifications', default=False, help='Send away email notifications.'),
    )

    def video_generator(self):
        """"""
        u = urllib.urlopen(TABINDEX_URL)
        file_data = u.read()
        lines = [x for x in file_data.split('\n') if x]
        data = [x.split('\t') for x in lines]
        fields, data = data[0], data[1:]
        fields = [i.lower() for i in fields]
        for line in data:
            yield dict(zip(fields, line))

    def _send_notification_emails(self, events):
        subscribers = {}
        for ev in events:
            for em in ev.emails.all():
                event_list = subscribers.setdefault(em.email, [])
                event_list.append(ev)

        for email, event_list in subscribers.iteritems():
            message = loader.render_to_string('org/video_published_email.txt', {
                'email': email,
                'events': event_list,
            })
            send_mail(u'[Kiberpipa] Sveže objavljeni posnetki dogodka', message, u'info@kiberpipa.org', [email])

    def handle(self, *args, **options):
        if options.get('notifications'):
            print 'Sending email notifications.'
            videos = Video.objects.filter(pub_date__lt=datetime.date.today(), pub_date__gte=datetime.date.today() - datetime.timedelta(1))
            events = [v.event for v in videos]
            self._send_notification_emails(events)
            return

        intranet_id_re = re.compile('\n\s*intranet-id:\s*(\d+)\s*\n*')

        for x in self.video_generator():
            try:
                pub_date = datetime.date(*time.strptime(x['day_published'], '%d.%m.%Y')[:3])

                vid, is_created = Video.objects.get_or_create(
                    videodir=x['id'],
                    defaults={
                        'image_url': 'http://video.kiberpipa.org/media/%(id)s/image-t.jpg' % x,
                        'pub_date': pub_date,
                        'play_url': 'http://video.kiberpipa.org/media/%(id)s/play.html' % x,
                    },
                )

                # fetch info.txt to see if intranet id is set
                info_data = urllib.urlopen(INFOTXT_URL % (x['id'],)).read()
                m = intranet_id_re.search(info_data, re.I | re.M | re.S)
                if m:
                    vid.event = Event.objects.get(pk=int(m.group(1)))
                vid.save()

            except Exception, e:
                print x, e
