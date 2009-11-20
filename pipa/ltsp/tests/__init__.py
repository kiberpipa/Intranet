import datetime
import md5
import simplejson
from django.test import TestCase

class TestLTSP(TestCase):
	
	def test_background(self):
		response = self.client.get('/services/ltsp/background.png')
		self.failUnlessEqual(response.status_code, 200)
		self.failUnlessEqual(response.get('content-type', None), 'image/png')
	
	def test_usage_report(self):
		from django.conf import settings
		url = '/services/ltsp/usage/'
		response = self.client.get(url)
		self.failUnlessEqual(response.status_code, 404)
		
		data = {'time': datetime.datetime.now().timetuple()[:7], 'count': 10}
		json_data = simplejson.dumps(data)
		sign = md5.new(json_data + settings.LTSP_USAGE_SECRET).hexdigest()
		
		response = self.client.post(url, {'data': json_data, 'sign': sign})
		self.failUnlessEqual(response.status_code, 200)
		resp = simplejson.loads(response.content)
		self.failUnlessEqual(resp['status'], 'ok')



