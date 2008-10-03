#!/usr/bin/env python

#called as post-commit script for intranet ci
import sys

from intranet.org.models import Project, Diary

from django.contrib.auth.models import User


user = User.objects.get(username=sys.argv[1])
intranet = Project.objects.get(id=2)
log_formal = sys.argv[2]
log_formal += '\nchangeset: https://www.kiberpipa.org/projekti/intranet/changeset/%s\n' % sys.argv[3]
diary = Diary(log_formal=log_formal, author=user, length='00:00:00', task=intranet)
diary.save()
