from django.db import models
from django.contrib.auth.models import User

class SalaryType(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class CostCenter(models.Model):
	name = models.CharField(max_length=200)
	wage_per_hour = models.DecimalField(max_digits=5, decimal_places=2)
	def __unicode__(self):
		return self.name

class MercenaryMonth(models.Model):
	"""
	Idea is to keep old data archived
	"""
	person = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	salary_type = models.ForeignKey(SalaryType, null=True)
	cost_center = models.ForeignKey(CostCenter, null=True)
	wage_per_hour = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	description = models.TextField(default='')
	month = models.DateField()
	
	def __unicode__(self):
		return u'MercenaryMonth: %s' % (str(self.person),)
		return u'MercenaryMonth: %s (%s/%s): %s' % (self.person, self.month.month, self.month.year, self.amount)


