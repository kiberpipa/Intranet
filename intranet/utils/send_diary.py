#!/usr/bin/env python

import datetime
import sys

from django.db.models import Q
from django.core.mail import send_mail

from intranet.org.models import Scratchpad, Diary, Lend

now = datetime.date.today() - datetime.timedelta(1)

result = 'Kiberpipa, dnevno porocilo: %d-%d-%d\n\n' % (now.year, now.month, now.day)

result += '=== Kracarka:\n\n%s\n\n' % Scratchpad.objects.all()[0].content

result += '=== Preteceni reverzi\n'

for lend in Lend.objects.filter(returned=False):
    result += '%s - %s posodil %s\n' % (lend.what, lend.to_who, lend.from_who)

result += '\n\n\nDnevniki:\n\n'

diarys = Diary.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day)
if not diarys:
    sys.exit(0)

for diary in diarys:
    result  += '[ %s - %s - %s - %s ]\n --\n %s \n--\n %s\n\n' % (diary.date, diary.author, diary.task.__unicode__(), diary.length, diary.log_formal, diary.log_informal)

send_mail('<insert something smart> %d-%d-%d' % (now.year, now.month, now.day), result, 'intranet@kiberpipa.org', ['pipa-org@list.kiss.si'])

