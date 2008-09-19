#!/usr/bin/env python

import MySQLdb

from intranet.www.models import News

from django.template.defaultfilters import slugify

con = MySQLdb.connect('127.0.0.1', 'root', 'b4l00n', 'webpage')
cur = con.cursor()

cur.execute('select pn_title, pn_time, pn_hometext, pn_sid from nuke_stories')

while 1:
    row = cur.fetchone()
    if not row: break
    News.objects.create(id=row[3], title=unicode(row[0], 'latin-1'), date=unicode(row[1].__str__(), 'latin-1'), text=unicode(row[2], 'latin-1'), slug=slugify(unicode(row[0], 'latin-1')))
