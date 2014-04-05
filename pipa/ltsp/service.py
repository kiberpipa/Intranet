# -*- coding: utf-8 -*-
from hashlib import md5
import os
import re
import datetime
import locale
from cStringIO import StringIO
import simplejson

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

from intranet.org.models import Event
from pipa.ltsp.models import Usage

TEMPLATE = os.path.join(os.path.dirname(__file__),'template.png')
FONTFILE = os.path.join(os.path.dirname(__file__),'FreeSansBold.ttf')

def ltsp_background_image(request):
	"""Generates a background PNG with events for this week."""
	upcoming_events = Event.objects.filter(public=True, start_date__gte=datetime.datetime.now()).order_by('start_date')[:6]
	
	orig_image = Image.open(TEMPLATE)
	image = orig_image.convert('RGB')
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype(FONTFILE, 25)
	
	# font colors
	fill = ('#FFFFFF', '#F5FF97')
	extra_color = '#FFC73B'
	y = 250
	x = 55
	draw.text((55, y-25), u'PRIHAJAJOČI DOGODKI', font=font, fill=extra_color)
	
	old_locale = locale.getlocale()
	if old_locale[0] == None:
		old_locale = 'C'
	elif old_locale[1] != None:
		old_locale = '%s.%s' % old_locale
	else:
		old_locale = old_locale[0]
	locale.setlocale(locale.LC_ALL, 'sl_SI.UTF-8')
	for i, e in enumerate(upcoming_events):
		y += 45
		cajt = e.start_date.strftime('%a. %d.%m. ob %H:%M')
		cajt = cajt[0].upper() + cajt[1:]
		event_line = u'%s, %s' % (e.title, cajt.decode('utf-8'))
		
		# check if line is too long, if it is, split in two lines
		m = re.match('(.{60,}?)[,](.*)', event_line)
		
		if m:
			first, second = m.groups()
			draw.text((x, y), first, font=font, fill=fill[i%2])
			y += 25
			draw.text((x, y), u' '*27 + second, font=font, fill=fill[i%2])
		else:
			draw.text((x, y), event_line, font=font, fill=fill[i%2])
	
	font22 = ImageFont.truetype(FONTFILE, 22)
	draw.text((x+45, y+80), u'Vstop na vse dogodke iz programa je prost,', font=font22, fill=fill[0])
	draw.text((x+93, y+104), u'več na', font=font22, fill=fill[0])
	draw.text((x+168, y+104), u'www.kiberpipa.org', font=font22, fill=extra_color)
	
	locale.setlocale(locale.LC_ALL, old_locale)
	stringio = StringIO()
	image.save(stringio, 'png')
	content = stringio.getvalue()
	
	response = HttpResponse(content, mimetype="image/png")
	return response

def internet_usage_report(request):
	"""
	LTSP reporting internet usage.
	
	To use it, you need to do a POST request with parameters
	data and sign, data is json encoded dict with datetime and count.
	Example:
	
	 {'time': [2009, 3, 2, 22, 37, 23, 0], 'count': 10}
	
	sign(ature) is a MD5 hash of serialized JSON with appended shared secret.
	"""
	if not request.method == 'POST':
		raise Http404
	
	data = request.POST.get('data', None)
	sign = request.POST.get('sign', None)
	
	if not data or not sign:
		return HttpResponse(simplejson.dumps({'status': 'fail'}))
	
	try:
		json = simplejson.loads(data)
	except ValueError:
		return HttpResponse(simplejson.dumps({'status': 'fail'}))
	t, all = json.get('time', ''), json.get('count', 0)
	
	if sign == md5.new(data + settings.LTSP_USAGE_SECRET).hexdigest():
		cnt = Usage(time=datetime.datetime(*t), count=all)
		cnt.save()
	else:
		return HttpResponse(simplejson.dumps({'status': 'fail'}))
	return HttpResponse(simplejson.dumps({'status': 'ok'}))

