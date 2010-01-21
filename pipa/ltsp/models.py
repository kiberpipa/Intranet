
from django.db import models

class Usage(models.Model):
	count = models.CommaSeparatedIntegerField(max_length=200)
	time = models.DateTimeField()
	
	def __unicode__(self):
		return u'LTSP usage: %s %s' % (self.time, self.count)
