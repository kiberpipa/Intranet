# *-* coding: utf-8 *-*

import urllib
import re
import datetime
import time
import logging

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template import loader

from pipa.video.models import Video
from intranet.org.models import Event


logger = logging.getLogger(__name__)
TABINDEX_URL = 'http://video.kiberpipa.org/tabindex.txt'
INFOTXT_URL = 'http://video.kiberpipa.org/media/%s/info.txt'
INTRANETID_REGEX = re.compile('\n\s*intranet-id:\s*(\d+)\s*\n*')


class Command(BaseCommand):
    """Parse videoarchive, store metadata and send notifications"""

    def parse_videoarchive(self):
        """"""
        u = urllib.urlopen(TABINDEX_URL)
        file_data = u.read()
        lines = [x for x in file_data.split('\n') if x]
        data = [x.split('\t') for x in lines]
        fields, data = data[0], data[1:]
        fields = [i.lower() for i in fields]
        for line in data:
            yield dict(zip(fields, line))

    def parse_intranet_id(self, id_):
        """fetch info.txt to see if intranet id is set"""
        info_data = urllib.urlopen(INFOTXT_URL % id_).read()
        m = INTRANETID_REGEX.search(info_data, re.I | re.M | re.S)
        if m:
            # this might be an error
            try:
                return Event.objects.get(pk=int(m.group(1)))
            except Event.DoesNotExist:
                logger.error('Wrong intranet id in videoarchive', extra=locals())

    def send_notification_emails(self, videos):
        subscribers = {}
        for video in videos:
            if video.event is None:
                logger.error('Video is not asigned to any event', extra={'video': video})
                continue
            for em in video.event.emails.all():
                event_list = subscribers.setdefault(em.email, [])
                event_list.append(video.event)

        for email, event_list in subscribers.iteritems():
            message = loader.render_to_string('video/video_published_email.txt', {
                'email': email,
                'events': event_list,
            })
            send_mail(
                subject=u'[Kiberpipa] Sveže objavljeni posnetki dogodka',
                message=message,
                from_email=u'info@kiberpipa.org',
                recipient_list=[email],
                fail_silently=True,
            )

    def handle(self, *a, **kw):
        videos_to_notify = []
        for x in self.parse_videoarchive():
            try:
                vid, is_created = Video.objects.get_or_create(
                    videodir=x['id'],
                    defaults={
                        'image_url': 'http://video.kiberpipa.org/media/%(id)s/image-t.jpg' % x,
                        'pub_date': datetime.date(*time.strptime(x['day_published'], '%d.%m.%Y')[:3]),
                        'play_url': 'http://video.kiberpipa.org/media/%(id)s/play.html' % x,
                    },
                )

                if vid.event is None:
                    vid.event = self.parse_intranet_id(x['id'])
                    if vid.event is not None:
                        # trigger notifications even if only intranet id was updated
                        is_created = True
                vid.save()

                if is_created:
                    videos_to_notify.append(vid)
            except:
                logger.error('Could not parse videoarchive: %s' % x, exc_info=True, extra=locals())

        self.send_notification_emails(videos_to_notify)
