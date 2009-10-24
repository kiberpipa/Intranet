
TABINDEX = 'http://video.kiberpipa.org/tabindex.txt'

from django.core.management.base import BaseCommand

class Command(BaseCommand):
	
	def handle(self, *args, **options):
		print options
		
		from pipa.video.models import Video
		from intranet.org.models import Event
		
		
		
