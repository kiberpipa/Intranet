from django.template import Context, Library, RequestContext
from django import template
from django import forms
from django.forms import FormWrapper
from django.template import resolve_variable
from django.conf import settings

register = Library()

from django.views.generic.list_detail import object_list

def print_video_object(object):
    return {'object': object, 'media_url': settings.MEDIA_URL, }
register.inclusion_tag('video/print_video_object.html')(print_video_object)

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

#    print kwargs
    return kwargs

class VideoBoxListNode(template.Node):
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
        #context['today'] = datetime.date.today()
        return template.loader.get_template(template_name).render(context)

def video_box_list(parser, token):
      bits = token.split_contents()
      object_name = bits[1]
      queryset = bits[2][1:-1]
      if len(bits) > 3:
          params = bits[3][1:-1]
      else:
          params = ''
      m = __import__("intranet.video.models", '','', object_name)
      object = getattr(m, object_name)
      return VideoBoxListNode(object, queryset, params)
register.tag('video_box_list', video_box_list)
