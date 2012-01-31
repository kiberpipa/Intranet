# *-* coding: utf-8 *-*

import datetime

from django.test import TestCase

from intranet.org.models import Event


class WWWTestCase(TestCase):
    fixtures = ['test_command_parse_videoarhive.json']

    def test_index(self):
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_ajax_index_events(self):
        # test zero events
        resp = self.client.get('/ajax/index/events', follow=True)
        self.assertFalse(resp.context.get('next', None))
        self.assertEqual(resp.status_code, 200)

        # add events and test full view
        event = Event.objects.get(id=1)
        event.start_date = datetime.datetime.now() + datetime.timedelta(1)
        event.save()

        resp = self.client.get('/ajax/index/events', follow=True)
        self.assertTrue(resp.context.get('next', None))
        self.assertEqual(resp.status_code, 200)
