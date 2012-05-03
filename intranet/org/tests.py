# *-* coding: utf-8 *-*

import re
import os
import simplejson
import datetime

from django.core.management import call_command
from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User

from intranet.org.models import Place, Project, Category, TipSodelovanja, IntranetImage, Diary


TESTUSER = 'testuser'
TESTPASSWORD = 'testpass'
EXAMPLE_GITHUB_COMMIT_HOOK = """
{
  "before": "5aef35982fb2d34e9d9d4502f6ede1072793222d",
  "repository": {
    "url": "http://github.com/defunkt/github",
    "name": "github",
    "description": "You're lookin' at it.",
    "watchers": 5,
    "forks": 2,
    "private": 1,
    "owner": {
      "email": "chris@ozmm.org",
      "name": "defunkt"
    }
  },
  "commits": [
    {
      "id": "41a212ee83ca127e3c8cf465891ab7216a705f59",
      "url": "http://github.com/defunkt/github/commit/41a212ee83ca127e3c8cf465891ab7216a705f59",
      "author": {
        "email": "chris@ozmm.org",
        "name": "Chris Wanstrath"
      },
      "message": "okay i give in",
      "timestamp": "2008-02-15T14:57:17-08:00",
      "added": ["filepath.rb"]
    },
    {
      "id": "de8251ff97ee194a289832576287d6f8ad74e3d0",
      "url": "http://github.com/defunkt/github/commit/de8251ff97ee194a289832576287d6f8ad74e3d0",
      "author": {
        "email": "chris@ozmm.org",
        "name": "Chris Wanstrath"
      },
      "message": "update pricing a tad",
      "timestamp": "2008-02-15T14:36:34-08:00"
    }
  ],
  "after": "de8251ff97ee194a289832576287d6f8ad74e3d0",
  "ref": "refs/heads/master"
}
"""


# TODO: deprecate this with fixtures
class BaseCase(TestCase):
    def ensure_test_user(self):
        try:
            User.objects.get(username=TESTUSER)
        except User.DoesNotExist:
            user = User.objects.create_user(username=TESTUSER,
                                            email='testuser@nonexistant.com')
            user.set_password(TESTPASSWORD)
            user.is_staff = True
            user.is_active = True
            user.first_name = "Chris"
            user.last_name = "Wanstrath"
            user.save()


class IndexTest(BaseCase):
    def test_index(self):
        self.client.login(username=TESTUSER, password=TESTPASSWORD)

        resp = self.client.get('/intranet/', follow=True)
        self.assertEqual(resp.status_code, 200)


class EventTest(BaseCase):
    def setUp(self):
        self.ensure_test_user()
        self.user = User.objects.get(username=TESTUSER)
        self.place = Place(name='Kiberpipa', note='Bla')
        self.place.save()
        self.project = Project(id=23, name='Tehnicarjenje', responsible=self.user)
        self.project.save(200)
        self.category = Category(name='Drugo', note='Another bla.')
        self.category.save()
        self.tip = TipSodelovanja(name="Predavatelj")
        self.tip.save()

    def create_new_image(self):
        self.client.login(username=TESTUSER, password=TESTPASSWORD)

        resp = self.client.get('/intranet/image_crop_tool/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/intranet/tmp_upload/', {'foo': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(simplejson.loads(resp.content)['status'], 'fail')

        # TODO: test .png
        f = open(os.path.join(os.path.dirname(__file__), 'test_fixtures', 'sample-1.jpg'), 'rb')
        resp = self.client.post('/intranet/tmp_upload/', {'image': f})
        f.close()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(simplejson.loads(resp.content)['status'], 'ok')
        self.assertTrue('temporary_filename' in self.client.session)
        filename = simplejson.loads(resp.content)['filename']

        self.assertEqual(self.client.session.get('temporary_filename'), filename)

        resp = self.client.post('/intranet/image_crop_tool/resize/', {'resize': '12,253,10,129', 'filename': filename, 'enter_your_email': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(simplejson.loads(resp.content)['status'], 'ok')
        resized_filename = simplejson.loads(resp.content)['resized_filename']

        resp = self.client.post('/intranet/image_crop_tool/save/', {'resized_filename': resized_filename, 'title': 'To je naslov slike.', 'enter_your_email': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(simplejson.loads(resp.content)['status'], 'ok')

        self.image_id = IntranetImage.objects.all()[0].id

    def test_event_lifetime(self):
        self.client.login(username=TESTUSER, password=TESTPASSWORD)

        self.create_new_image()

        resp = self.client.get('/intranet/events/create/')
        self.assertEqual(resp.status_code, 200)

        now = datetime.datetime.now()
        tomorrow_noon = datetime.datetime(now.year, now.month, now.day, 12, 0) + datetime.timedelta(2)
        tomorrow_noon_fifteen = datetime.datetime(now.year, now.month, now.day, 13, 0) + datetime.timedelta(2)

        createdata = {
            'event_repeat': 0,
            'event_repeat_freq': 1,
            'event_repeat_freq_type': 0,
            'title': u'Dogodek v Kleti',
            'project': self.project.id,
            'authors': u'Gašper Žejn - Predavatelj',
            'tip': 1,
            'category': self.category.id,
            'language': 'sl',
            'responsible': 1,
            'public': 'on',
            'start_date': tomorrow_noon.strftime('%Y/%m/%d %H:%M'),
            'end_date': tomorrow_noon_fifteen.strftime('%Y/%m/%d %H:%M'),
            'require_technician': 'on',
            'require_video': 'on',
            'place': self.place.id,
            'slides': '',
            'event_image': self.image_id,
            'announce': 'Test event for intranet tests.',
            'note': '',
            'enter_your_email': '',
        }
        resp = self.client.post('/intranet/events/create/', createdata)
        self.assertEqual(resp.status_code, 302)
        # if we don't get location, form failed
        redirect_url, event_id = re.match('https://.+(/intranet/events/(\d+)/edit/)$', resp._headers['location'][1]).groups()

        # validate urls
        self.assertEqual(self.client.get('/event/dogodek-v-kleti-1/', follow=True).redirect_chain[-1], ('http://testserver/sl/event/dogodek-v-kleti-1/', 302))

        resp = self.client.get(redirect_url)
        self.assertEqual(resp.status_code, 200)

        # new event is in the events overview page
        resp = self.client.get('/intranet/events/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(redirect_url) > -1, True)

        # TODO: test archive events

        # add emails to be notified
        email = 'root@kiberpipa.org'
        resp = self.client.post('/intranet/events/%s/emails/' % event_id, {'emails': email, 'enter_your_email': ''}, follow=True)
        self.assertEqual(resp.status_code, 200)

        # volunteer
        resp = self.client.get('/intranet/events/%s/technician/take/' % event_id, follow=True)
        self.assertEqual(resp.status_code, 200)

        # TODO: test if techie is set
        self.assertTrue(resp.content.find('%s/technician/cancel/' % event_id) > 0)

        # cancel
        resp = self.client.get('/intranet/events/%s/technician/cancel/' % event_id, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('%s/technician/cancel/' % event_id), -1)

        # add diary
        diarydata = {
            'log_formal': 'no kidding',
            'log_informal': 'just joking',
            'length': '4',
            'uniqueSpot': event_id,
            'enter_your_email': '',
        }
        resp = self.client.post('/intranet/tehniki/add/', diarydata, follow=True)
        self.assertEqual(resp.status_code, 200)

        # test ical
        resp = self.client.get('/sl/calendar/ical/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp._headers['content-type'][1].startswith('text/calendar'), True)


class DiaryTest(BaseCase):
    def setUp(self):
        self.ensure_test_user()
        self.project = Project(name='Videoarhiv')
        self.project.save()

        self.project2 = Project(name='Intranet')
        self.project2.save()
        # TODO: fixtures

    def test_commit_hook(self):
        resp = self.client.post('/intranet/diarys/commit_hook/', {'payload': EXAMPLE_GITHUB_COMMIT_HOOK})
        self.assertEqual(resp.status_code, 403)

        resp = self.client.post('/intranet/diarys/commit_hook/', {'payload': EXAMPLE_GITHUB_COMMIT_HOOK}, REMOTE_ADDR="207.97.227.253")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'OK')

        diary = Diary.objects.all()[0]
        self.assertTrue("Commit: okay i give in" in diary.log_formal)
        self.assertTrue("Commit: update pricing a tad" in diary.log_formal)

    def test_diary(self):
        self.client.login(username=TESTUSER, password=TESTPASSWORD)

        resp = self.client.get('/intranet/diarys/')
        self.assertEqual(resp.status_code, 200)

        now = datetime.datetime.now()
        diary_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)

        diarydata = {
            'date': diary_day.strftime('%d.%m.%Y %H:%M:%S'),
            'log_formal': 'to je formalni dnevnik',
            'log_informal': 'to je neformalni dnevnik',
            'length': '04:00:00',
            'task': self.project.id,
            'enter_your_email': '',  # honeypot
        }
        resp = self.client.post('/intranet/diarys/add/', diarydata)
        self.assertEqual(resp.status_code, 302)
        redirect_url, diary_id = re.match('http://\w+(/intranet/diarys/(\d+)/)$', resp._headers['location'][1]).groups()

        resp = self.client.get(redirect_url)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/intranet/diarys/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(redirect_url) > -1, True)

        updatedata = diarydata.copy()
        updatedata['log_formal'] = 'to je *NOVI* formalni dnevnik'
        resp = self.client.post('/intranet/diarys/%s/edit/' % diary_id, updatedata)
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post('/intranet/diarys/', {'author': '', 'task': self.project.id, 'enter_your_email': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(redirect_url) > -1, True)

        # TODO: test archive diary


class CommandsTest(BaseCase):
    # ./manage.py dumpdata --indent=1 org.Diary org.Scratchpad
    fixtures = ['test_send_diary.json']

    def setUp(self):
        self.ensure_test_user()

    def test_send_diary(self):
        call_command('send_diary', '17.12.2010')
        self.assertEqual(len(mail.outbox), 1)


class ParseVideoArhivTest(BaseCase):
    fixtures = ['test_command_parse_videoarhive.json']

    def setUp(self):
        self.ensure_test_user()

    def test_parse_empty_videoarhiv(self):
        # TODO: mock http request
        call_command('parse_videoarhiv')
        self.assertEqual(len(mail.outbox), 0)
