#!/usr/bin/env python

import MySQLdb
import sys

from intranet.www.models import News
from django.utils.encoding import *
from django.template.defaultfilters import slugify

#pw = sys.stdin.readline()

con = MySQLdb.connect('127.0.0.1', 'root', '', 'webpage', use_unicode=False)
cur = con.cursor()

cur.execute('select pn_title, pn_time, pn_hometext, pn_sid from nuke_stories')

while 1:
    row = cur.fetchone()
    if not row: break
    encoding = 'latin2'
    
    row0 = smart_unicode(row[0], encoding=encoding, strings_only=False, errors='strict')
    row1 = smart_unicode(row[1], encoding=encoding, strings_only=False, errors='strict')
    row2 = smart_unicode(row[2], encoding=encoding, strings_only=False, errors='strict')
    row3 = smart_unicode(row[3], encoding=encoding, strings_only=False, errors='strict')
    
    News.objects.create(id=row3, title=row0, date=row1.__str__(), text=row2, slug=slugify(row0) )

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

cur.execute('select pc_eid, pc_title, pc_time, pc_hometext from `nuke_postcalendar_events` where pc_eid not in ('+ ','.join(equal) +')')

while 1:
    row = cur.fetchone()
    if not row: break
    encoding = 'latin2'
    
    calendar_id = smart_unicode(row[0], encoding=encoding, strings_only=False, errors='strict')
    title = smart_unicode(row[1], encoding=encoding, strings_only=False, errors='strict')
    time = smart_unicode(row[2], encoding=encoding, strings_only=False, errors='strict')
    text = smart_unicode(row[3], encoding=encoding, strings_only=False, errors='strict')

    News.objects.create(calendar_id=calendar_id, title=title, date=time.__str__(), text=text, slug=slugify(title) )
