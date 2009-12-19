import datetime
from cStringIO import StringIO

from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


from pipa.mercenaries.models import MercenaryMonth
from pipa.mercenaries.xls import salary_xls

def _recalculate_mercenarymonth(year, month):
	from intranet.org.models import Diary
	diaries = Diary.objects.filter(pub_date__year=year, pub_date__month=month)
	
	MercenaryMonth.objects.filter(month__year=year, month__month=month).delete()
	mercenaries = {}
	for d in diaries:
		mercenary = mercenaries.get(d.author.id, None)
		if mercenary is None:
			mercenary, created = MercenaryMonth.objects.get_or_create(person=d.author)
		
		if d.task.cost_center:
			mercenary.wage_per_hour = d.task.cost_center.wage_per_hour
			mercenary.cost_center = d.task.cost_center
			mercenary.salary_type = d.task.salary_type
			# XXX: currently only full hours count
			mercenary.amount += d.length.hour * mercenary.wage_per_hour
			mercenary.hours += d.length.hour
			# XXX
		mercenaries[d.author.id] = mercenary
	
	for author, m in mercenaries.iteritems():
		m.save()

def index(request, year, month):
	today = datetime.date.today()
	if year == None:
		return HttpResponseRedirect('%s/%s/' % (today.year, today.month))
	
	year = int(year)
	month = int(month)
	if today.year == year and today.month == month:
		_recalculate_mercenarymonth(year, month)
	
	# XXX: Lookup by month triggers a bug in SQLite3 backend on Django 1.0, very much like bug #3501
	mercenaries = MercenaryMonth.objects.filter(month__year=year, month__month=month)
	
	total = 0
	for m in mercenaries:
		total += m.amount
	
	context = {
		'add_link': '%s/intranet/admin/org/mercenary/add/' % settings.BASE_URL,
		'mercenaries': mercenaries,
		'year': year,
		'month': month,
		'all': total,
		'hmonth': datetime.datetime(int(year), int(month), 1).strftime('%B'),
		}
	
	return render_to_response("mercenaries/index.html", RequestContext(request, context))
index = login_required(index)

def export_xls(request, year, month, id):
	year = int(year)
	month = int(month)
	today = datetime.date.today()
	if today.year == year and today.month == month:
		_recalculate_mercenarymonth(year, month)
	
	compact = False
	if id == 'compact':
		compact = True
	filename = 'place_%d_%d' % (month, year)
	
	params = []
	
	for m in MercenaryMonth.objects.filter(month__year=year, month__month=month):
		params.append({'mercenary': m.person.get_full_name(),
			'amount': m.amount,
			'hours': m.hours,
			'cost_center': unicode(m.cost_center),
			'salary_type': unicode(m.salary_type),
			'description': unicode(m.description),
			})
	
	output = StringIO()
	output.write(salary_xls(compact=compact, bureaucrat=request.user.get_full_name(), params=params))
	response = HttpResponse(mimetype='application/octet-stream')
	response['Content-Disposition'] = "attachment; filename=" + filename + '.xls'
	response.write(output.getvalue())
	output.close()
	return response
export_xls = login_required(export_xls)

