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

    def test_public_event(self):
        resp = self.client.get('/event/blabla-1/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(resp.redirect_chain, [
            ('http://testserver/sl/event/blabla-1/', 302),
            ('http://testserver/sl/event/test-77-3-1/', 302),
        ])

        resp = self.client.get('/sl/event/test-77-3-1/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(resp.redirect_chain, [])

        resp = self.client.get('/sl/event/2011-jan-01/1/blabla/hopsasa/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(resp.redirect_chain, [
            ('http://testserver/event/blabla-1/', 301),
            ('http://testserver/sl/event/blabla-1/', 302),
            ('http://testserver/sl/event/test-77-3-1/', 302),
        ])
