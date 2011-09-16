# *-* coding: utf-8 *-*

import re
import os
import simplejson
import datetime

from django.core.management import call_command
from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User

from intranet.org.models import Place, Project, Category, TipSodelovanja, IntranetImage


TESTUSER = 'testuser'
TESTPASSWORD = 'testpass'


# TODO: deprecate this with fixtures
class BaseCase(TestCase):
    def ensure_test_user(self):
        try:
            User.objects.get(username=TESTUSER)
        except User.DoesNotExist:
            user = User.objects.create_user(username=TESTUSER, email='testuser@nonexistant.com')
            user.set_password(TESTPASSWORD)
            user.is_staff = True
            user.is_active = True
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

        f = open(os.path.join(os.path.dirname(__file__), 'test_fixtures', 'test.png'), 'rb')
        resp = self.client.post('/intranet/tmp_upload/', {'image': f})
        f.close()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(simplejson.loads(resp.content)['status'], 'ok')
        self.assertTrue('temporary_filename' in self.client.session)
        filename = simplejson.loads(resp.content)['filename']

        self.assertEqual(self.client.session.get('temporary_filename'), filename)

        resp = self.client.post('/intranet/image_crop_tool/resize/', {'resize': '90,253,44,129', 'filename': filename})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(simplejson.loads(resp.content)['status'], 'ok')
        resized_filename = simplejson.loads(resp.content)['resized_filename']

        resp = self.client.post('/intranet/image_crop_tool/save/', {'resized_filename': resized_filename, 'title': 'To je naslov slike.'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(simplejson.loads(resp.content)['status'], 'ok')

        self.image_id = IntranetImage.objects.all()[0].id

    def test_event_lifetime(self):
        self.client.login(username=TESTUSER, password=TESTPASSWORD)

        self.create_new_image()

        resp = self.client.get('/intranet/events/create/')
        self.assertEqual(resp.status_code, 200)

        now = datetime.datetime.now()
        tomorrow_noon = datetime.datetime(now.year, now.month, now.day, 12, 0) + datetime.timedelta(1)

        createdata = {
            'event_repeat': 0,
            'event_repeat_freq': 1,
            'event_repeat_freq_type': 0,
            'title': u'Dogodek v Kleti',
            'project': self.project.id,
            'author': u'Gašper Žejn',
            'tip': 1,
            'category': self.category.id,
            'language': 'sl',
            'responsible': TESTUSER,
            'public': '',
            'start_date': tomorrow_noon.strftime('%Y-%m-%d %H:%M'),
            'require_technician': 'on',
            'require_video': 'on',
            'place': self.place.id,
            'slides': '',
            'event_image': self.image_id,
            'announce': 'Test event for intranet tests.',
            'note': '',
        }
        resp = self.client.post('/intranet/events/create/', createdata)
        self.assertEqual(resp.status_code, 302)
        # if we don't get location, form failed
        redirect_url, event_id = re.match('http://\w+(/intranet/events/(\d+)/)$', resp._headers['location'][1]).groups()

        # validate urls
        self.assertEqual(self.client.get('/event/dogodek-v-kleti-1/', follow=True).redirect_chain[-1], ('http://testserver/sl/event/dogodek-v-kleti-1/', 301))
        self.assertEqual(self.client.get('/event/2001-jul-06/1/dogodek-v-kleti/', follow=True).redirect_chain[-1], ('http://testserver/sl/event/dogodek-v-kleti-1/', 302))

        resp = self.client.get(redirect_url)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(redirect_url + 'info.txt/')
        self.assertEqual(resp.status_code, 200)
        for line in [i for i in resp.content.split('\n') if i]:
            self.assertEqual(re.match('^\S+:\s', line) != None, True)

        # autocomplete should work now because a sodelovanje was added
        resp = self.client.get('/intranet/autocomplete/person/', {'q': u'Gašp'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('\n' in resp.content, True)

        # new event is in the events overview page
        resp = self.client.get('/intranet/events/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(redirect_url) > -1, True)

        # add a number of visitors
        resp = self.client.post(redirect_url + 'count/', {'visitors': 10})
        self.assertEqual(resp.status_code, 302)
        a_redirect_url, _ = re.match('http://\w+(/intranet/events/(\d+)/)$', resp._headers['location'][1]).groups()
        self.assertEqual(a_redirect_url, redirect_url)

        # add emails to be notified
        email = 'root@kiberpipa.org'
        resp = self.client.post('/intranet/events/%s/emails/' % event_id, {'emails': email}, follow=True)
        self.assertEqual(resp.status_code, 200)

        # check that email is listed
        resp = self.client.get('/intranet/events/%s/' % event_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(email) > -1, True)

        # tehniki
        resp = self.client.get('/intranet/tehniki/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(redirect_url) > -1, True)
        self.assertEqual(resp.content.find('/intranet/tehniki/add/%s/' % event_id) > -1, True)

        # volunteer
        resp = self.client.get('/intranet/tehniki/add/%s/' % event_id, follow=True)
        self.assertEqual(resp.status_code, 200)

        # check volunteering
        resp = self.client.get('/intranet/tehniki/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('/intranet/tehniki/cancel/%s/' % event_id) > -1, True)

        # cancel
        resp = self.client.get('/intranet/tehniki/cancel/%s/' % event_id, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('/intranet/tehniki/cancel/%s/' % event_id), -1)

        # add diary
        diarydata = {
            'log_formal': 'no kidding',
            'log_informal': 'just joking',
            'length': '4',
            'uniqueSpot': event_id,
        }
        resp = self.client.post('/intranet/tehniki/add/', diarydata, follow=True)
        self.assertEqual(resp.status_code, 200)

        # check monthly view
        month = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'avg', 'sep', 'okt', 'nov', 'dec'][tomorrow_noon.month - 1]
        resp = self.client.get('/intranet/tehniki/%s/%s/' % (tomorrow_noon.year, month))
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

    def test_diary(self):
        self.client.login(username=TESTUSER, password=TESTPASSWORD)

        resp = self.client.get('/intranet/diarys/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/intranet/diarys/add/')
        self.assertEqual(resp.status_code, 200)

        now = datetime.datetime.now()
        diary_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)

        diarydata = {
            'date': diary_day.strftime('%d.%m.%Y %H:%M:%S'),
            'log_formal': 'to je formalni dnevnik',
            'log_informal': 'to je neformalni dnevnik',
            'length': '04:00:00',
            'task': self.project.id,
        }
        resp = self.client.post('/intranet/diarys/add/', diarydata)
        self.assertEqual(resp.status_code, 302)
        redirect_url, diary_id = re.match('http://\w+(/intranet/diarys/(\d+)/)$', resp._headers['location'][1]).groups()

        resp = self.client.get(redirect_url)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/intranet/diarys/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(redirect_url) > -1, True)

        resp = self.client.get('/intranet/diarys/%s/edit/' % diary_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(diarydata['log_formal']) > -1, True)

        updatedata = diarydata.copy()
        updatedata['log_formal'] = 'to je *NOVI* formalni dnevnik'
        resp = self.client.post('/intranet/diarys/%s/edit/' % diary_id, updatedata)
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post('/intranet/diarys/', {'author': '', 'task': self.project.id})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find(redirect_url) > -1, True)


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
        call_command('parse_videoarhiv')
        self.assertEqual(len(mail.outbox), 3)
