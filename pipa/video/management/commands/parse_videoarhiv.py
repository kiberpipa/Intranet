
TABINDEX = 'http://video.kiberpipa.org/tabindex.txt'

from django.core.management.base import BaseCommand

TABINDEX_URL = 'http://video.kiberpipa.org/tabindex.txt'
INFOTXT_URL = 'http://video.kiberpipa.org/media/%s/info.txt'

class Command(BaseCommand):
	
	def video_generator(self):
		import urllib
		u = urllib.urlopen(TABINDEX_URL)
		file_data = u.read()
		lines = [x for x in file_data.split('\n') if x]
		data = [x.split('\t') for x in lines]
		fields, data = data[0], data[1:]
		fields = [i.lower() for i in fields]
		for line in data:
			yield dict(zip(fields, line))
	
	def handle(self, *args, **options):
		print options
		
		from pipa.video.models import Video
		from intranet.org.models import Event
		import urllib
		import re
		import datetime
		import time
		
		intranet_id_re = re.compile('\n\s*intranet-id:\s*(\d+)\s*\n*')
		
		for x in self.video_generator():
			try:
				pub_date = datetime.date(*time.strptime(x['day_published'], '%d.%m.%Y')[:3])
			except Exception, e:
				print x, e
				continue
			
			try:
				vid = Video.objects.get(videodir=x['id'])
			except Video.DoesNotExist:
				vid = Video.objects.create(
					videodir=x['id'],
					image_url='http://video.kiberpipa.org/media/%(id)s/image-t.jpg' % x,
					pub_date=pub_date,
					play_url='http://video.kiberpipa.org/media/%(id)s/play.html' % x,
					)
			
			# fetch info.txt to see if intranet id is set
			try:
				u = urllib.urlopen(INFOTXT_URL % (x['id'],))
				info_data = u.read()
				m = intranet_id_re.search(info_data, re.I | re.M | re.S)
				if m:
					vid.event = Event.objects.get(pk=int(m.group(1)))
			except Exception, e:
				print x['id'], e
			
			vid.save()
		
