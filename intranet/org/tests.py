# *-* coding: utf-8 *-*
import unittest

from django.test.client import Client

TESTUSER = 'testuser'
TESTPASSWORD = 'testpass'

def ensure_test_user():
	from django.contrib.auth.models import User
	try:
		User.objects.get(username=TESTUSER)
	except User.DoesNotExist:
		user = User.objects.create_user(username=TESTUSER, email='testuser@nonexistant.com')
		user.set_password(TESTPASSWORD)
		user.is_staff = True
		user.is_active = True
		user.save()

class IndexTest(unittest.TestCase):
	def runTest(self):
		c = Client()
		c.login(username=TESTUSER, password=TESTPASSWORD)
		
		resp = c.get('/intranet/')
		self.assertEqual(resp.status_code, 200)

class EventTest(unittest.TestCase):
	def setUp(self):
		ensure_test_user()
		from django.contrib.auth.models import User
		from intranet.org.models import Place, Project, Category, TipSodelovanja
		self.user = User.objects.get(username=TESTUSER)
		self.place = Place(name='Kiberpipa', note='Bla')
		self.place.save()
		self.project = Project(id=23, name='Tehnicarjenje', responsible=self.user)
		self.project.save()
		self.category = Category(name='Drugo', note='Another bla.')
		self.category.save()
		self.tip = TipSodelovanja(name="Predavatelj")
		self.tip.save()
	
	def create_new_image(self):
		import os
		import simplejson
		c = Client()
		c.login(username=TESTUSER, password=TESTPASSWORD)
		
		resp = c.get('/intranet/image_crop_tool/')
		self.assertEqual(resp.status_code, 200)
		
		resp = c.post('/intranet/tmp_upload/', {'foo': ''})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(simplejson.loads(resp.content)['status'],'fail')
		
		f = open(os.path.join(os.path.dirname(__file__), 'test.png'), 'rb')
		resp = c.post('/intranet/tmp_upload/', {'image': f})
		f.close()
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(simplejson.loads(resp.content)['status'],'ok')
		self.assertEqual(c.session.has_key('temporary_filename'), True)
		filename = simplejson.loads(resp.content)['filename']
		
		self.assertEqual(c.session.get('temporary_filename'), filename)
		
		resp = c.post('/intranet/image_crop_tool/resize/', {'resize': '90,253,44,129', 'filename': filename})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(simplejson.loads(resp.content)['status'],'ok')
		resized_filename = simplejson.loads(resp.content)['resized_filename']
		
		resp = c.post('/intranet/image_crop_tool/save/', {'resized_filename': resized_filename, 'title': 'To je naslov slike.'})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(simplejson.loads(resp.content)['status'],'ok')
		
		from intranet.org.models import IntranetImage
		self.image_id = IntranetImage.objects.all()[0].id
	
	def testEventLifeTime(self):
		import datetime
		import re
		c = Client()
		c.login(username=TESTUSER, password=TESTPASSWORD)
		
		self.create_new_image()
		
		resp = c.get('/intranet/events/create/')
		self.assertEqual(resp.status_code, 200)
		
		now = datetime.datetime.now()
		tomorrow_noon = datetime.datetime(now.year, now.month, now.day, 12, 0) + datetime.timedelta(1)
		
		createdata = {
			'event_repeat': 0,
			'event_repeat_freq': 1,
			
			'event_repeat_freq_type': 0,
			'end_date': '',
			'title': u'Dogodek v Kleti',
			'project': self.project.id,
			'author': u'Gašper Žejn',
			'tip': 1,
			'category': self.category.id,
			'language': 'sl',
			'responsible': self.user.id,
			'public': '',
			'start_date': tomorrow_noon.strftime('%Y-%m-%d %H:%M'),
			'length': '01:00:00',
			'require_technician': 'on',
			'require_video': 'on',
			'place': self.place.id,
			'slides': '',
			'event_image': self.image_id,
			'announce': 'Test event for intranet tests.',
			'short_announce': '',
			'note': '',
		}
		resp = c.post('/intranet/events/create/', createdata)
		self.assertEqual(resp.status_code, 302)
		redirect_url, event_id = re.match('http://\w+(/intranet/events/(\d+)/)$', resp._headers['location'][1]).groups()
		
		resp = c.get(redirect_url)
		self.assertEqual(resp.status_code, 200)
		
		resp = c.get(redirect_url + 'info.txt/')
		self.assertEqual(resp.status_code, 200)
		for line in [i for i in resp.content.split('\n') if i]:
			self.assertEqual(re.match('^\S+:\s', line) != None, True)
		
		# autocomplete should work now because a sodelovanje was added
		resp = c.get('/intranet/autocomplete/person/', {'q': u'Gašp'})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual('\n' in resp.content, True)
		
		# new event is in the events overview page
		resp = c.get('/intranet/events/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find(redirect_url) > -1, True)
		
		# add a number of visitors
		resp = c.post(redirect_url + 'count/', {'visitors': 10})
		self.assertEqual(resp.status_code, 302)
		a_redirect_url, _ = re.match('http://\w+(/intranet/events/(\d+)/)$', resp._headers['location'][1]).groups()
		self.assertEqual(a_redirect_url, redirect_url)
		
		# add emails to be notified
		email = 'root@kiberpipa.org'
		resp = c.post('/intranet/events/%s/emails/' % event_id, {'emails': email})
		self.assertEqual(resp.status_code, 302)
		
		# check that email is listed
		resp = c.get('/intranet/events/%s/' % event_id)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find(email) > -1, True)
		
		# tehniki
		resp = c.get('/intranet/tehniki/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find(redirect_url) > -1, True)
		self.assertEqual(resp.content.find('/intranet/tehniki/add/%s/' % event_id) > -1, True)
		
		# volunteer
		resp = c.get('/intranet/tehniki/add/%s/' % event_id)
		self.assertEqual(resp.status_code, 302)
		
		# check volunteering
		resp = c.get('/intranet/tehniki/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find('/intranet/tehniki/cancel/%s/' % event_id) > -1, True)
		
		# cancel
		resp = c.get('/intranet/tehniki/cancel/%s/' % event_id)
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.content.find('/intranet/tehniki/cancel/%s/' % event_id), -1)
		
		# add diary
		diarydata = {
			'length': 2,
			'log_formal': 'no kidding',
			'log_informal': 'just joking',
			'uniqueSpot': event_id
		}
		resp = c.post('/intranet/tehniki/add/', diarydata)
		self.assertEqual(resp.status_code, 302)
		
		# check monthly view
		month = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'avg', 'sep', 'okt', 'nov', 'dec'][tomorrow_noon.month-1]
		resp = c.get('/intranet/tehniki/%s/%s/' % (tomorrow_noon.year, month))
		self.assertEqual(resp.status_code, 200)
		
		# test ical
		resp = c.get('/sl/calendar/ical/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp._headers['content-type'][1].startswith('text/calendar'), True)
		

class DiaryTest(unittest.TestCase):
	def setUp(self):
		ensure_test_user()
		from intranet.org.models import Project
		self.project = Project(name='Videoarhiv')
		self.project.save()
	
	def testDiary(self):
		import datetime
		import re
		c = Client()
		c.login(username=TESTUSER, password=TESTPASSWORD)
		
		resp = c.get('/intranet/diarys/')
		self.assertEqual(resp.status_code, 200)
		
		resp = c.get('/intranet/diarys/add/')
		self.assertEqual(resp.status_code, 200)
		
		now = datetime.datetime.now()
		diary_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
		
		diarydata = {
			'date': diary_day.strftime('%Y-%m-%d %H:%M:%S'),
			'length': '04:00:00',
			'log_formal': 'to je formalni dnevnik',
			'log_informal': 'to je neformalni dnevnik',
			'task': self.project.id,
		}
		resp = c.post('/intranet/diarys/add/', diarydata)
		self.assertEqual(resp.status_code, 302)
		redirect_url, diary_id = re.match('http://\w+(/intranet/diarys/(\d+)/)$', resp._headers['location'][1]).groups()
		
		resp = c.get(redirect_url)
		self.assertEqual(resp.status_code, 200)
		
		resp = c.get('/intranet/diarys/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find(redirect_url) > -1, True)
		
		resp = c.get('/intranet/diarys/%s/edit/' % diary_id)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find(diarydata['log_formal']) > -1, True)
		
		updatedata = diarydata.copy()
		updatedata['log_formal'] = 'to je *NOVI* formalni dnevnik'
		resp = c.post('/intranet/diarys/%s/edit/' % diary_id, updatedata)
		self.assertEqual(resp.status_code, 302)
		
		resp = c.post('/intranet/diarys/', {'author':'', 'task': self.project.id})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find(redirect_url) > -1, True)
	
