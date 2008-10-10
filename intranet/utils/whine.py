#!/usr/bin/env python

#usage: whine.py <number of days>


from datetime import datetime, timedelta
import sys

from django.core.mail import send_mail

from intranet.org.models import Bug


try:
    days = int(sys.argv[1])
except IndexError:
    days = 1


today = datetime.today()
whine = today - timedelta(days)

bugz = Bug.objects.filter(due_by__lte = whine, resolution__resolved=False)

for bug in bugz:
    bug.mail(subject='reminder')
