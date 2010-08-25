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
	
	def testUpload(self):
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
		




