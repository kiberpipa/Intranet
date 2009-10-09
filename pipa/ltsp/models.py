
from django.db import models

class Usage(models.Model):
	count = models.CommaSeparatedIntegerField(max_length=200)
	time = models.DateTimeField()
