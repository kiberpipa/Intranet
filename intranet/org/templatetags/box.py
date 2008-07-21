from django.template import Context, Library, RequestContext
from django import template
from django import oldforms as forms
from django.oldforms import FormWrapper
from django.template import resolve_variable, Variable
from django.core.exceptions import ObjectDoesNotExist

from intranet.org.models import Event, Bug, Scratchpad, Resolution
from intranet.localsettings import MEDIA_URL
import datetime

register = Library()

from django.views.generic.list_detail import object_list

def loadcomments(object, user):
    return {'object': object, 'user': user }
register.inclusion_tag('org/showcomments.html')(loadcomments)

def box_change_diary():
    return { }
register.inclusion_tag('org/box_diary_change.html')(box_change_diary)

def box_plache(diarys, user):
    list = {}
    paylist = {}
    objects = []
    total = 0
    sum = 0
    for o in diarys:

        a = o.author.username
        if list.has_key(a):
            list[a] += o.length.hour 
        else:
            list[a] = o.length.hour 
            paylist[a] = 0
        if o.task.id <= 2:
            paylist[a] += o.length.hour 

    for o in list:
        a = {}
        a['name'] = o
        a['time'] = list[o]
        a['paytime'] = paylist[o]
        a['money'] = paylist[o] * 3.13
        objects.append(a)
        total += list[o]
        sum += (paylist[o] * 3.13)
    return {'objects': objects,
            'user': user,
            'total': total,
            'sum': sum }

register.inclusion_tag('org/box_plache.html')(box_plache)

def box_bug_stats(user):
    all = Bug.objects.all()
    allopen = all.count()
    #open = Bug.objects.filter(resolved__exact=False)
    open = Bug.objects.filter(resolution__isnull = True )
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

def print_diary(form):
    return {'object': form }
register.inclusion_tag('org/print_diary.html')(print_diary)

def print_shopping(object):
    return {'object': object }
register.inclusion_tag('org/print_shopping.html')(print_shopping)

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

class BoxAddNode(template.Node):
    def __init__(self, object, parent='', edit=False):
        self.object = object
        self.edit = edit
        if parent:
            self.parent = Variable(parent)
        else:
            self.parent = parent

    def render(self, context):
        manipulator = self.object.AddManipulator()
        if self.parent:
            self.parent =  self.parent.resolve(context)
        if self.edit:
            form = forms.FormWrapper(manipulator, Bug.objects.get(pk=self.parent).__dict__, {})
            print 'teh form'
            print Bug.objects.get(pk=self.parent).assign.all()
            print form['assign']
            #form['assign_id'] = form['assign']
            #print form['assign_id']
            c = Context({'form':form, 'edit': True})
        else:
            form = forms.FormWrapper(manipulator, {}, {})
            c = Context({'form':form, 'parent': self.parent,})
        return template.loader.get_template('org/box_%s.html' % self.object._meta.object_name.lower()).render(c)

def box_add(parser, token):
    args = token.split_contents()
    box_name = args[1]
    m = __import__("intranet.org.models", '','', box_name)
    object = getattr(m, box_name)
    if len(args) == 3:
        return BoxAddNode(object, parent=args[2])
    elif len(args) == 4:
        return BoxAddNode(object, parent=args[2], edit=True)
    else:
        return BoxAddNode(object)
register.tag('box_add', box_add)

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

        for i in kwargs:
            if kwargs[i] == 'False':
              kwargs[i] = False
            elif kwargs[i] == 'True':
              kwargs[i] = True
            else:
              kwargs[i] = resolve_variable(kwargs[i], context)
        kwargs = dict([(str(x),kwargs[x]) for x in kwargs.keys()]) 
        
        new_queryset = self.object.objects.filter(**kwargs)
        
        pargs = parse(self.params)
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
