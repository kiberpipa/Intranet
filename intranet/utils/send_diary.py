#!/usr/bin/env python

import datetime

from django.db.models import Q
from django.core.mail import send_mail

from intranet.org.models import Scratchpad, Diary, Lend

now = datetime.date.today()
y = now - datetime.timedelta(1)

result = 'Kiberpipa, dnevno porocilo: %d-%d-%d\n\n' % (now.year, now.month, now.day)

result += '=== Kracarka:\n\n%s\n\n' % Scratchpad.objects.all()[0].content

result += '=== Preteceni reverzi\n'

for lend in Lend.objects.filter(returned=False):
    result += '%s - %s posodil %s\n' % (lend.what, lend.to_who, lend.from_who)

result += '\n\n\nDnevniki:\n\n'

for diary in Diary.objects.filter(Q(date__year=now.year, date__month=now.month, date__day=now.day) | Q(date__year=y.year, date__month=y.month, date__day=y.day)):
    if diary.date.date() == y and diary.date.hour < 6:
        continue
    result  += '[ %s - %s - %s - %s ]\n --\n %s \n--\n %s\n\n' % (diary.date, diary.author, diary.task.__unicode__(), diary.length, diary.log_formal, diary.log_informal)

send_mail('intranet spam', result, 'intranet@kiberpipa.org', ['redduck666@gmail.com'])

