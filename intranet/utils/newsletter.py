#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import sys

from django.core.mail import send_mail
from django.template.defaultfilters import capfirst
from django.contrib.sites.models import Site
from django.conf import settings

from intranet.org.models import Event, Sodelovanje
from intranet.www.templatetags.www import truncchar, sanitize_html


#run with LC_ALL=sl_SI.UTF-8
import locale
locale.resetlocale() 

now = datetime.date.today()
week = now + datetime.timedelta(7)

events = Event.objects.filter(start_date__range=(now, week))

trenutna_stran = Site.objects.get(id=settings.SITE_ID)

if not events:
    sys.exit(0)

result = u''

for i in events:
    result += capfirst(unicode(i.start_date.strftime('%A, %d. %b. %Y %H:%M\n'), 'utf-8'))
    result += '%s: %s\n' % (unicode(i.project), unicode(i.title))
    predavatelji = [unicode(s.person.name) for s in Sodelovanje.objects.filter(event=i, tip=1)]
    if predavatelji:
        result += ', '.join(predavatelji)
        result += '\n'
    moderatorji = [unicode(s.person.name) for s in Sodelovanje.objects.filter(event=i, tip=3)]
    if moderatorji:
        result += 'moderira '
        result += ', '.join(moderatorji)
        result += '\n'
    result += '\n\n'
    result += truncchar(sanitize_html(i.announce), 250)
    result += u'\n\n\nVeč o tem:\nhttp://%s%s\n' % (trenutna_stran.domain, i.get_public_url())
    result += i.start_date.strftime('\n\n//////////////////////////////////////////////////\n\n')


result += u"""


Kiberpipa
Kersnikova 6
1000 Ljubljana
pon.-pet.:  10.00 - 22.00
prost vstop / prost dostop / prosto programje
info at kiberpipa.org

Spletna stran: http://www.kiberpipa.org/
Videoarhiv, prenos v živo: http://video.kiberpipa.org/
Twitter: http://twitter.com/Kiberpipa
Facebook rsvp - skupine: Kiberpipa, Spletne urice in Pipini odprti termini, Filmsteka


--


Kiberpipo podpirajo: Zavod K6/4, ŠOU v Ljubljani, Evropski sklad za
regionalni razvoj, Ministrstvo za visoko šolstvo, znanost in tehnologijo
- projekt E-točke, Ministrstvo za kulturo RS in Mestna občina Ljubljana.
Kiberpipa je članica Mreže multimedijskih centrov Slovenije M3C in
Društva Asociacija.
"""

send_mail('<insert something smart> %d-%d-%d' % (now.year, now.month, now.day), result, 'intranet@kiberpipa.org', ['almir@kiberpipa.org'])
