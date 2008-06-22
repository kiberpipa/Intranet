#!/usr/bin/env python

#usage: whine.py <number of days>


from datetime import datetime, timedelta
import smtplib, sys

from django.db.models import Q

from intranet.org.models import Bug


try:
    days = int(sys.argv[1])
except IndexError:
    days = 1


today = datetime.today()
whine = today - timedelta(days)

bugz = Bug.objects.filter(Q(due_by__gt = whine) | Q(due_by__lt = today))


##construct the mail bodies
mails = {}
for bug in bugz:
    assignees = ''
    for assignee in bug.assign.all():
        assignees += assignee.__unicode__()

    for assignee in bug.assign.all():
        mail = assignee.get_profile().mail
        try:
            mails[mail] += 'bug #%i\n' % bug.id
        except KeyError:
            mails[mail] = ''
            mails[mail] += 'bug #%i\n' % bug.id

        mails[mail] += 'bug url: %s\n' % bug.get_absolute_url() 
        mails[mail] += 'assigned to: %s\n' % assignees
        mails[mail] += 'reported by: %s\n' % bug.author
        mails[mail] += 'DEADLINE: %s\n' % bug.due_by
        mails[mail] += '\n\n'

for to in mails:
    
        mail_from = 'intranet@kiberpipa.org'
        msg = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % (mail_from, to, 'reminder', mails[to])


        session = smtplib.SMTP('localhost')
        session.sendmail(mail_from, to, msg)
        session.close()

