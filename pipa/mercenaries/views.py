import datetime
from cStringIO import StringIO

from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


from pipa.mercenaries.models import MercenaryMonth, FixedMercenary, CostCenter, SalaryType
from pipa.mercenaries.xls import salary_xls

def _recalculate_mercenarymonth(year, month):
	from intranet.org.models import Diary
	diaries = Diary.objects.filter(date__year=year, date__month=month)
	
	MercenaryMonth.objects.filter(month__year=year, month__month=month, mercenary_type=MercenaryMonth.TYPE_HOURLY).delete()
	the_month = datetime.date(year, month, 1)
	mercenaries = {}
	for d in diaries:
		mercenary = mercenaries.get(d.author.id, None)
		if mercenary is None:
			mercenary, created = MercenaryMonth.objects.get_or_create(person=d.author, month=the_month)
		
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
	
	today = datetime.date.today()
	if today.month == month and today.year == year:
		# XXX FIXME: hardcoded
		cost_ctr = CostCenter.objects.get(id=2)
		slry = SalaryType.objects.get(id=2)
		for fm in FixedMercenary.objects.all():
			try:
				mm = MercenaryMonth.objects.get(person=fm.person)
			except MercenaryMonth.DoesNotExist:
				mm = MercenaryMonth(person=fm.person, amount=fm.amount, hours=1,
						wage_per_hour=fm.amount, month=the_month, mercenary_type=MercenaryMonth.TYPE_FIXED, cost_center=cost_ctr, salary_type=slry)
				mm.save()

def index(request, year, month):
	today = datetime.date.today()
	if year == None:
		return HttpResponseRedirect('%s/%s/' % (today.year, today.month))
	
	recalculation_msg = ''
	
	year = int(year)
	month = int(month)
	if today.year == year and today.month == month:
		_recalculate_mercenarymonth(year, month)
	elif request.POST:
		if request.POST.get('recalculate'):
			prev_month = today - datetime.timedelta(today.day + 1)
			if (year, month) in ((today.year, today.month), (prev_month.year, prev_month.month)):
				_recalculate_mercenarymonth(year, month)
			else:
				recalculation_msg = u'Sorry. You can only recalculate previous month.'
	
	# XXX: Lookup by month triggers a bug in SQLite3 backend on Django 1.0, very much like bug #3501
	mercenaries = MercenaryMonth.objects.filter(month__year=year, month__month=month)
	
	total = 0
	last_calculated = datetime.datetime(2000,1,1,0,0,0)
	for m in mercenaries:
		if m.salary_type_id in (None, 1):
			total += m.amount
			if m.last_calculated != None and last_calculated < m.last_calculated:
				last_calculated = m.last_calculated
	
	context = {
		'add_link': '/intranet/admin/mercenaries/fixedmercenary/', # XXX ugly
		'mercenaries': mercenaries,
		'year': year,
		'month': month,
		'all': total,
		'hmonth': datetime.datetime(int(year), int(month), 1).strftime('%B'),
		'last_calculated': last_calculated,
		'recalculation_msg': recalculation_msg,
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
	filename = 'place_redni_%d_%d' % (month, year)
	mtype = MercenaryMonth.TYPE_FIXED
	if id == 'napotnice':
		compact = True
		filename = 'napotnice_%d_%d' % (month, year)
		mtype = MercenaryMonth.TYPE_HOURLY
	
	params = []
	
	for m in MercenaryMonth.objects.filter(month__year=year, month__month=month, mercenary_type=mtype):
		if m.amount > 0:
			params.append({'mercenary': m.person.get_full_name(),
				'amount': m.amount,
				'hours': m.hours,
				'cost_center': unicode(m.cost_center),
				'salary_type': unicode(m.salary_type),
				'description': unicode(m.cost_center.description),
				})
	
	output = StringIO()
	if params:
		output.write(salary_xls(compact=compact, bureaucrat=request.user.get_full_name(), params=params))
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = "attachment; filename=" + filename + '.xls'
	response.write(output.getvalue())
	output.close()
	return response
export_xls = login_required(export_xls)

