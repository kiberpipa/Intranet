from optparse import make_option
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option('--event', action='store_true', dest='twit_event', default=False, help='twit live stream (default if --event not specified) or events'),
	)
	
	def handle(self, *args, **options):
		import datetime
		from os.path import join
		import simplejson
		import twitter
		from urllib2 import urlopen
		
		from django.conf import settings
		from intranet.org.models import Event, Sodelovanje
		
		twit_event = options.get('twit_event')
		
		def get_bitly_url(url):
			dump = urlopen('http://api.bit.ly/shorten?version=2.0.0&long_url=' + url +'&login=crkn&api_key=R_678ce6a3bba1c3f64f996080e21909c2')
			return simplejson.loads(dump.read())['results'][url]['hashUrl']
		
		api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
		today = datetime.datetime.today()
		events = Event.objects.filter(public=True, start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
		
		if twit_event:
			#the announce event tweet
			for e in events:
				short_url = get_bitly_url(join(settings.BASE_URL + e.get_public_url()[1:])) #compensate for two slashes
				
				sodelovanja = ''
				if Sodelovanje.objects.filter(event=e).count() == 1:
					sodelovanja = '- ' + Sodelovanje.objects.filter(event=e)[0].person.name
				
				if e.language == 'SI':
					api.PostUpdate(u'%s danes ob %s:%.2d #Kiberpipa: %s %s %s' % (
						e.project, e.start_date.hour, e.start_date.minute, e.title, sodelovanja, short_url))
				else:
					api.PostUpdate(u'%s today at %s:%.2d #Kiberpipa: %s %s %s' % (
						e.project, e.start_date.hour, e.start_date.minute, e.title, sodelovanja, short_url))
		else:
			#the live stream announcement
			min_15 = today + datetime.timedelta(seconds=15*60)
			events = events.filter(require_video=True, start_date__range=(today, min_15))
			for e in events:
				short_url = get_bitly_url(join(settings.BASE_URL + e.get_public_url()[1:])) #compensate for two slashes
				
				sodelovanja = ''
				if Sodelovanje.objects.filter(event=e).count() == 1:
					sodelovanja = Sodelovanje.objects.filter(event=e)[0].person.name + ' '
				
				if e.language == 'EN':
					api.PostUpdate(u'%slive from #Kiberpipa (%s: %s): at http://bit.ly/FdgZ' % (
						sodelovanja, unicode(e.project), e.title))
				else:
					api.PostUpdate(u'%sv zivo iz #Kiberpipa (%s: %s): na http://bit.ly/FdgZ' % (
						sodelovanja, unicode(e.project), e.title))
