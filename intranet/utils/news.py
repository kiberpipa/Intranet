#!/usr/bin/env python

# Migracija starih novic v novo bazo, the Django waii

import MySQLdb
import sys

from intranet.www.models import News


from django.utils.encoding import *
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

#pw = sys.stdin.readline()

# Connect more bit unicode free (default forca utf-8), zato use_unicode=False
# V nasprotnem primeru se ze tu polomijo podatki zaradi razlicnega charseta

con = MySQLdb.connect('127.0.0.1', 'root', '', 'webpage', use_unicode=False)
cur = con.cursor()

katja = User.objects.get(pk=19)

cur.execute('select pn_title, pn_time, pn_hometext, pn_sid, pn_informant from nuke_stories')

# Tole je Almir while while zanke...strange, but works
while 1:
    row = cur.fetchone()
    if not row: break
    encoding = 'latin2' # Precej pomembna rec... encoding podatkov v nasi bazi - ce je to narobe, se stvari zbrejkajo
    
    # Za smart_unicode funkcijo glej django unicode dokumentacijo
    row0 = smart_unicode(row[0], encoding=encoding, strings_only=False, errors='strict') 
    row1 = smart_unicode(row[1], encoding=encoding, strings_only=False, errors='strict')
    row2 = smart_unicode(row[2], encoding=encoding, strings_only=False, errors='strict')
    row3 = smart_unicode(row[3], encoding=encoding, strings_only=False, errors='strict')
    row4 = smart_unicode(row[4], encoding=encoding, strings_only=False, errors='strict')
    try:
        user = User.objects.get(username=row4)
    except User.DoesNotExist:
        user = katja
    
    News.objects.create(id=row3, title=row0, date=row1.__str__(), text=row2, slug=slugify(row0), author=user)

##handle the calendar entries with the same title's as news
equal=[]
cur.execute('SELECT `nuke_stories`.`pn_sid` , `nuke_postcalendar_events`.`pc_eid` FROM nuke_postcalendar_events, nuke_stories WHERE `nuke_stories`.`pn_title` = `nuke_postcalendar_events`.`pc_title`')

while 1:
    row = cur.fetchone()
    if not row: break
    equal += [str(row[1])]
    n = News.objects.get(id=row[0])
    n.calendar_id = row[1]
    n.save()

#na koncu se calendar entryje ki jih ni ratalo zlinkat z novicami
cur.execute('select pc_eid, pc_title, pc_time, pc_hometext, pc_informant from `nuke_postcalendar_events` where pc_eid not in ('+ ','.join(equal) +')')

while 1:
    row = cur.fetchone()
    if not row: break
    encoding = 'latin2'
    
    calendar_id = smart_unicode(row[0], encoding=encoding, strings_only=False, errors='strict')
    title = smart_unicode(row[1], encoding=encoding, strings_only=False, errors='strict')
    time = smart_unicode(row[2], encoding=encoding, strings_only=False, errors='strict')
    text = smart_unicode(row[3], encoding=encoding, strings_only=False, errors='strict')
    username = smart_unicode(row[3], encoding=encoding, strings_only=False, errors='strict')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = katja

    News.objects.create(calendar_id=calendar_id, title=title, date=time.__str__(), text=text, slug=slugify(title), author=user)
