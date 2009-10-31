# -*- coding: utf-8 -*-
import os
import re
import datetime
import locale
from cStringIO import StringIO

from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont

from intranet.org.models import Event

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
	
	locale.setlocale(locale.LC_ALL, 'sl_SI')
	for i, e in enumerate(upcoming_events):
		y += 45
		cajt = e.start_date.strftime('%a. %d.%m. ob %H:%M')
		cajt = cajt[0].upper() + cajt[1:]
		event_line = '%s: %s' % (e.title, cajt)
		
		# check if line is too long, if it is, split in two lines
		m = re.match('(.{70,})[,:](.*)', event_line)
		
		if m:
			first, second = m.groups()
			draw.text((x, y), first, font=font, fill=fill[i%2])
			x += 25
			draw.text((x, y), u' '*27 + second, font=font, fill=fill[i%2])
		else:
			draw.text((x, y), event_line, font=font, fill=fill[i%2])
	
	font22 = ImageFont.truetype(FONTFILE, 22)
	draw.text((x+45, y+80), u'Vstop na vse dogodke iz programa je prost,', font=font22, fill=fill[0])
	draw.text((x+93, y+104), u'več na', font=font22, fill=fill[0])
	draw.text((x+168, y+104), u'www.kiberpipa.org', font=font22, fill=extra_color)
	
	stringio = StringIO()
	image.save(stringio, 'png')
	content = stringio.getvalue()
	
	response = HttpResponse(content, mimetype="image/png")
	return response
