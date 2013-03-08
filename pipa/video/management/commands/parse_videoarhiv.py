# *-* coding: utf-8 *-*

import urllib
import datetime
import time
import logging
import simplejson

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template import loader

from pipa.video.models import Video
from intranet.org.models import Event


logger = logging.getLogger(__name__)
JSON_URL = 'http://video.kiberpipa.org/site/api/lectures/public/?ordering=-time&page_size=50'


class Command(BaseCommand):
    """Parse videoarchive, store metadata and send notifications"""

    def parse_videoarchive(self):
        """"""
        u = urllib.urlopen(JSON_URL)
        data = simplejson.loads(u.read())
        return data['results']

    def send_notification_emails(self, videos):
        subscribers = {}
        for video in videos:
            if video.event is None:
                logger.error('Video is not asigned to any event', extra={'video': video})
                continue
            for em in video.event.emails.all():
                event_list = subscribers.setdefault(em.email, set())
                event_list.add(video.event)

        for email, event_list in subscribers.iteritems():
            message = loader.render_to_string('video/video_published_email.txt', {
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
            remote_ref = x.get('remote_ref', None)
            if not remote_ref:
                continue

            try:
                try:
                    event = Event.objects.get(pk=int(remote_ref))
                except Event.DoesNotExist:
                    logger.error('Wrong intranet id in videoarchive: %s' % x.get('remote_ref'), extra={'remote': x})
                    continue

                slug = x.get('slug')

                # because of legacy reasons, we have to be careful not to load
                # old videos that do not have remote_id set in DB, because they will be
                # readded
                vid, is_created = Video.objects.get_or_create(
                    remote_id=x['id'],
                    defaults={
                        'title': x.get('title'),
                        'event': event,
                        'image_url': 'http://video.kiberpipa.org/media/%s/image-i.jpg' % slug,
                        'pub_date': datetime.date(*time.strptime(x['published'], '%Y-%m-%d')[:3]),
                        'play_url': 'http://video.kiberpipa.org/media/%s/play.html' % slug,
                    },
                )

                # TODO: if event now has a video, and require_video is False, set it to True!
                # TODO: also write a migration for this.

                if is_created:
                    videos_to_notify.append(vid)
            except:
                logger.error('Could not parse videoarchive: %s' % x, exc_info=True, extra=locals())

        self.send_notification_emails(videos_to_notify)
