from django.template import Context, Library, RequestContext
from django import template
from django import forms
from django.forms import FormWrapper
from django.template import resolve_variable

from intranet.org.models import Event as org_event
from intranet.k4.models import Event as k4_event
from intranet.kapelica.models import Event as kapelica_event
from intranet.k6_4 import feedparser

import datetime

register = Library()

from django.views.generic.list_detail import object_list

def load_first_post():
    d = feedparser.parse("http://www.k6-4.org/?feed=atom")
    date = d['entries'][0]['date']
    content = d['entries'][0]['content'][0]['value']
    title = d['entries'][0]['title']
    link = d['entries'][0]['link']
    return {'post_date': date,
            'post_content': content,
            'post_title': title,
            'post_link': link,
            }
register.inclusion_tag('k6_4/post.html')(load_first_post)

def current_events():
    today = datetime.date.today()
    limit = today + datetime.timedelta(days=7)

    kiberpipa = org_event.objects.filter(start_date__range=(today,limit)).order_by('start_date').values('start_date', 'id', 'title')

    klub = k4_event.objects.filter(start_date__range=(today,limit)).order_by('start_date').values('start_date', 'id', 'title')

    galerija = kapelica_event.objects.filter(start_date__range=(today,limit)).order_by('start_date').values('start_date', 'id', 'title')

    list = []
    for p in kiberpipa:
        p['what'] = 'intranet'
        list.append(p)
    for p in klub:
        p['what'] = 'k4'
        list.append(p)
    for p in galerija:
        p['what'] = 'kapelica'
        list.append(p)

    return {'list': list,
            }
register.inclusion_tag('k6_4/list_event.html')(current_events)

def print_event(form):
    return {'event': form }
register.inclusion_tag('k6_4/print_event.html')(print_event)

