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

class UploadTest(unittest.TestCase):
	def setUp(self):
		ensure_test_user()
	
	def runTest(self):
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

class EventTest(unittest.TestCase):
	def setUp(self):
		ensure_test_user()
		from django.contrib.auth.models import User
		from intranet.org.models import Place, Project, Category, TipSodelovanja
		self.user = User.objects.get(username=TESTUSER)
		self.place = Place(name='Kiberpipa', note='Bla')
		self.place.save()
		self.project = Project(name='Kiberpipa', responsible=self.user)
		self.project.save()
		self.category = Category(name='Drugo', note='Another bla.')
		self.category.save()
		self.tip = TipSodelovanja(name="Predavatelj")
		self.tip.save()
		from intranet.org.models import IntranetImage
		UploadTest().runTest()
		self.image_id = IntranetImage.objects.all()[0].id

	
	def testEventLifeTime(self):
		import datetime
		import re
		c = Client()
		c.login(username=TESTUSER, password=TESTPASSWORD)
		
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
		resp = c.get('/intranet/autocomplete/', {'q': u'Gašp'})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual('\n' in resp.content, True)
		
		resp = c.get('/intranet/events/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content.find(redirect_url) > -1, True)
		
