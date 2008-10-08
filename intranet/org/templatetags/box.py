#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.template import Context, Library, RequestContext
from django import template
from django.template import resolve_variable, Variable
from django.core.exceptions import ObjectDoesNotExist

from intranet.org.models import Event, Bug, Scratchpad, Resolution
from intranet.localsettings import MEDIA_URL
import datetime
import math

register = Library()

from django.views.generic.list_detail import object_list

@register.filter
def in_list(value,arg):
    return value in arg


def loadcomments(object, user):
    return {'object': object, 'user': user }
register.inclusion_tag('org/showcomments.html')(loadcomments)

# summarize paid, unpaid time for given period of diaries
def box_plache(diarys, user):
    list = {} 		# Hash<author.username, hours unpaid>
    paylist = {} 	# Hash<author.username, hours paid>
    billable_hours = 0	# total paid time, in hours
    total_hours = 0	# total paid+unpaid time, in hours
    sum = 0		# total to be paid (= total paid time * tariff)

    # pupulate list, paylist from diaries
    for o in diarys:
        print "DEBUG: God diary for event %s by %s, date %s" % (o.id, o.author.username, o.date)
        a = o.author.username
        if list.has_key(a):
            list[a] += o.length.hour 
        else:
            list[a] = o.length.hour 
            paylist[a] = 0
        total_hours += o.length.hour        
        
        # paid projects are dezuranje (22) and tehnicarjenje (23)
        # they must reference an event that requires a technician, also
        if ( (o.task.id == 22) or (o.task.id == 23 and o.event != None and (o.event.require_technician or o.event.require_video)) ):
            paylist[a] += o.length.hour
            billable_hours += o.length.hour
        

    # compute per-person summaries
    tariff = 3.50				# EUR/hour
    objects = []				# List<Hash<String, Object>> - summaries per person 
    for o in list:				# for every author.username
        a = {}					# his summary
        a['name'] = o
        a['time'] = list[o]			# unpaid time in hours
        a['paytime'] = paylist[o]		# paid time in hours
        a['money'] = paylist[o] * tariff	# paid time * tariff (3.13eur/h currently)
        objects.append(a)

        # add to totals
        sum += (paylist[o] * tariff)

    # sort by a['money']
    objects.sort(lambda a, b: int( b['money'] - a['money'] ))

    return {'objects': objects,
            'user': user,
            'billable_hours': billable_hours,
            'total_hours': total_hours,
            'sum': sum }


register.inclusion_tag('org/box_plache.html')(box_plache)

def box_bug_stats(user):
    all = Bug.objects.all()
    allopen = all.count()
    open = Bug.objects.filter(resolution__resolved=False)
    count = open.count()
    my = open.filter(assign__exact=user).count()
    mine = all.filter(assign__exact=user).count()

    if not mine:
      rate = str(0)
    else:
      rate = str(1 - float(my) / float(mine))[:4]

    if not allopen:
      grate = str(0)
    else:
      grate = str(1 - float(count) / float(allopen))[:4]

    return {'count': count,
            'my': my,
            'rate': rate,
            'grate': grate,
            'allopen': allopen,  }
register.inclusion_tag('org/box_bug_stats.html')(box_bug_stats)

def box_scratchpad(user):
    try:
      scratchpad = Scratchpad.objects.latest('id')
    except ObjectDoesNotExist:
      scratchpad = []
    
    return {'object': scratchpad}
register.inclusion_tag('org/box_scratchpad.html')(box_scratchpad)   

def print_shopping(object):
    return {'object': object }
register.inclusion_tag('org/print_shopping.html')(print_shopping)

def print_diary(form):
    return {'object': form }
register.inclusion_tag('org/print_diary.html')(print_diary)


def print_event(form):
    return {'event': form, 'media_url': MEDIA_URL }
register.inclusion_tag('org/print_event.html')(print_event)

def form_event(form):
    return {'form': form }
register.inclusion_tag('org/form_event.html')(form_event)

def form_shopping(form):
    return {'form': form }
register.inclusion_tag('org/form_shopping.html')(form_shopping)

def box_reccurings(form):
    return {'form': form }
register.inclusion_tag('org/box_reccurings.html')(box_reccurings)

def parse(args):
    kwargs = {}
    if args:
        if ',' not in args:
            # ensure at least one ','
            args += ','
        for arg in args.split(','):
            arg = arg.strip()
            if arg == '': continue
            kw, val = arg.split('=', 1)
            kw = kw.lower()
            kwargs[kw] = val

    return kwargs

class BoxListNode(template.Node):
    """
    Example usage:
        {% box_list ObjectName "QuerySet" ["template=foo,order_by=bar,limit=:3"] }
        In third parameter, template, order_by and limit are all optional.

        {% box_list Lend "returned=False,from_who__exact=user.id" "template=box/foo.html,order_by=returned,limit=:2" %}

        the templates get extra variable 'today' passed
    """
    def __init__(self, object, queryset, params):
        self.object = object
        self.queryset  = queryset
        self.params = params

    def render(self, context):
        kwargs = parse(self.queryset)
        pargs = parse(self.params)

        for i in kwargs:
            if kwargs[i] == 'False':
              kwargs[i] = False
            elif kwargs[i] == 'True':
              kwargs[i] = True
            else:
              kwargs[i] = resolve_variable(kwargs[i], context)
        kwargs = dict([(str(x),kwargs[x]) for x in kwargs.keys()]) 
        
        new_queryset = self.object.objects.filter(**kwargs)

        if pargs.has_key('order_by'):
            new_queryset = new_queryset.order_by(pargs['order_by'])

        if pargs.has_key('limit'):
            l = pargs['limit']
            i = l.split(':')[0]
            if i:
                i = int(i)
            else:
                i = 0
            j = l.split(':')[1]
            if j:
                j = int(j)
            else:
                j = 0
            new_queryset = new_queryset[i:j]

        if pargs.has_key('template'):
            template_name = pargs['template']
        else:
            model = new_queryset.model
            template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())

        context['object_list'] = new_queryset
        context['today'] = datetime.date.today()
        return template.loader.get_template(template_name).render(context)

def box_list(parser, token):
      bits = token.split_contents()
      object_name = bits[1]
      queryset = bits[2][1:-1]
      if len(bits) > 3:
          params = bits[3][1:-1]
      else:
          params = ''
      m = __import__("intranet.org.models", '','', object_name)
      object = getattr(m, object_name)
      return BoxListNode(object, queryset, params)
register.tag('box_list', box_list)
