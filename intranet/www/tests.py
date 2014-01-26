# *-* coding: utf-8 *-*

import datetime
import json as simplejson

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils.dateformat import format as format_
from intranet.org.models import Event


class WWWAjaxTestCase(TestCase):
    """Test case for Ajax features of www app."""

    fixtures = ['test_command_parse_videoarhive.json']

    def test_ajax_index_events_now(self):
        """Test ajax_index_events method with today == 'Sob, 16. nov'.

        Example of testing data `events_dict`:
        {'events': {'0': {'date': 'Pon, 11. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '11. 11.'},
            '1': {'date': 'Tor, 12. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '12. 11.'},
            '2': {'date': 'Sre, 13. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '13. 11.'},
            '3': {'date': u'\u010det, 14. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '14. 11.'},
            '4': {'date': 'Pet, 15. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '15. 11.'},
            '5': {'date': 'Sob, 16. nov',
                  'events': [],
                  'is_today': True,
                  'short_date': '16. 11.'},
            '6': {'date': 'Ned, 17. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '17. 11.'}},
         'next_url': 'https://example.com/ajax/index/events/2013/47/',
         'prev_url': 'https://example.com/ajax/index/events/2013/45/'}
        """
        resp = self.client.get('/ajax/index/events', follow=True)
        events_dict = simplejson.loads(resp.content)
        self.assertEqual(resp.status_code, 200)

        today = datetime.date.today()
        today_date = format_(today, 'D, d. b').capitalize()
        today_short_date = format_(today, 'd. n.')

        self.assertIn('events', events_dict)
        self.assertIn('next_url', events_dict)
        self.assertIn('prev_url', events_dict)
        for i in range(7):
            events_by_day = events_dict['events'][str(i)]

            self.assertIn('date', events_by_day)
            self.assertIn(type(events_by_day['date']), [unicode, str])

            self.assertIn('events', events_by_day)
            self.assertEqual(list, type(events_by_day['events']))

            self.assertIn('is_today', events_by_day)
            self.assertEqual(bool, type(events_by_day['is_today']))

            self.assertIn('short_date', events_by_day)
            self.assertIn(type(events_by_day['short_date']), [unicode, str])

            if events_by_day['is_today']:
                self.assertEqual(events_by_day['date'], today_date)
                self.assertEqual(events_by_day['short_date'], today_short_date)

    def test_ajax_index_events_future(self):
        """Test ajax_index_events method with tomorrow == 'Ned, 17. nov'.

        Example of testing data `events_dict`:
        {'events': {'0': {'date': 'Pon, 11. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '11. 11.'},
            '1': {'date': 'Tor, 12. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '12. 11.'},
            '2': {'date': 'Sre, 13. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '13. 11.'},
            '3': {'date': u'\u010det, 14. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '14. 11.'},
            '4': {'date': 'Pet, 15. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '15. 11.'},
            '5': {'date': 'Sob, 16. nov',
                  'events': [],
                  'is_today': False,
                  'short_date': '16. 11.'},
            '6': {'date': 'Ned, 17. nov',
                  'events': [],
                  'is_today': True,
                  'short_date': '17. 11.'}},
         'next_url': 'https://example.com/ajax/index/events/2013/47/',
         'prev_url': 'https://example.com/ajax/index/events/2013/45/'}
        """
        tomorrow = datetime.date.today() + relativedelta(days=1)
        tomorrow_date = format_(tomorrow, 'D, d. b').capitalize()
        tomorrow_short_date = format_(tomorrow, 'd. n.')

        event = Event.objects.get(id=1)
        event.start_date = tomorrow
        event.save()

        resp = self.client.get('/ajax/index/events', follow=True)
        events_dict = simplejson.loads(resp.content)
        self.assertEqual(resp.status_code, 200)

        self.assertIn('events', events_dict)
        self.assertIn('next_url', events_dict)
        self.assertIn('prev_url', events_dict)
        for i in range(7):
            events_by_day = events_dict['events'][str(i)]

            self.assertIn('date', events_by_day)
            self.assertIn(type(events_by_day['date']), [unicode, str])

            self.assertIn('events', events_by_day)
            self.assertEqual(list, type(events_by_day['events']))

            self.assertIn('is_today', events_by_day)
            self.assertEqual(bool, type(events_by_day['is_today']))

            self.assertIn('short_date', events_by_day)
            self.assertIn(type(events_by_day['short_date']), [unicode, str])

            if events_by_day['is_today']:
                self.assertEqual(events_by_day['date'], tomorrow_date)
                self.assertEqual(events_by_day['short_date'], tomorrow_short_date)


class WWWTestCase(TestCase):
    fixtures = ['test_command_parse_videoarhive.json']

    def test_index(self):
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_public_event(self):
        resp = self.client.get('/event/blabla-1/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/sl/event/test-77-3-1/')

        resp = self.client.get('/sl/event/test-77-3-1/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(resp.redirect_chain, [])

        resp = self.client.get('/sl/event/2011-jan-01/1/blabla/hopsasa/',
                               follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/sl/event/test-77-3-1/', status_code=301)

    def test_prostori(self):
        resp = self.client.get('/sl/prostori/2/opis.ajax', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_feeds(self):
        resp = self.client.get('/sl/feeds/novice/', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/sl/feeds/dogodki/', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/sl/feeds/pot/', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/sl/feeds/su/', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/sl/feeds/planet/', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/sl/feeds/muzej/', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/sl/feeds/all/', follow=True)
        self.assertEqual(resp.status_code, 200)
