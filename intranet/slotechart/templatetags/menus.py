from django import template
register = template.Library()
from django.conf import settings

from intranet.slotechart.models import TechArtProject, Festival

import datetime
from types import StringType

# ---- podrobnosti ----

def print_event(event):
    return {'object': event,
			'awards': event.award.all(),
			'gallerys': event.gallery_org.all(),
			'producers': event.producer_org.all(),
			'festivals': event.festival.all(),
			'artists': event.artist.all(),
			'collaborators': event.collaborator.all(),
			'media_url': settings.MEDIA_URL,
			}
register.inclusion_tag('slotechart/print_event.html')(print_event)

def simple_detail(object):
    events = object.techartproject_set.select_related()
    artists = {}
    for event in events:
        for collab in event.collaborator.all():
            artists[collab] = 1
        for artist in event.artist.all():
            artists[artist] = 1
    return {'object': object,
			'events': events,
			'artists': artists,
			'media_url': settings.MEDIA_URL,
			}
register.inclusion_tag('slotechart/print_detail.html')(simple_detail)

def producer_detail(object):
    events = object.producer.select_related()
    festivals = object.festival_producer.all()
    awards = {}
    artists = {}
    for event in events:
        for award in event.award.all():
            awards[award] = 1
        for collab in event.collaborator.all():
            artists[collab] = 1
        for artist in event.artist.all():
            artists[artist] = 1
    return {'object': object,
			'events': events,
			'festivals': festivals,
			'awards': awards,
			'artists': artists,
			'media_url': settings.MEDIA_URL,
			}
register.inclusion_tag('slotechart/print_detail.html')(producer_detail)

def artist_detail(object):
    events = object.techartproject_set.select_related() # collaborators field
    myevents = object.sloartist.select_related()		# artist field
    eventz = {}
    gallerys = {}
    festivals = {}
    awards = {}
    collaborators = {}
    producers = {}
    for event in events:
        eventz[event] = 1
        for collab in event.collaborator.all():
            if collab.name != object.name:
                collaborators[collab] = 1
        for artist in event.artist.all():
            if artist.name != object.name:
                collaborators[artist] = 1
        for festival in event.festival.all():
            festivals[festival] = 1
        for award in event.award.all():
            awards[award] = 1
    for event in myevents:
        eventz[event] = 1
        for gallery in event.gallery_org.all():
            gallerys[gallery] = 1
        for producer in event.producer_org.all():
            producers[producer] = 1
        for festival in event.festival.all():
            festivals[festival] = 1
        for award in event.award.all():
            awards[award] = 1
        for collab in event.collaborator.all():
            if collab.name != object.name:
                collaborators[collab] = 1
        for artist in event.artist.all():
            if artist.name != object.name:
                collaborators[artist] = 1
    return {'object': object,
			'events': eventz,
			'festivals': festivals,
			'gallerys': gallerys,
			'awards': awards,
			'collaborators': collaborators,
			'producers': producers,
			'media_url': settings.MEDIA_URL,
			}
register.inclusion_tag('slotechart/print_detail.html')(artist_detail)

def object_detail(object):
    events = object.techartproject_set.select_related()
    gallerys = {}
    festivals = {}
    awards = {}
    artists = {}
    collaborators = {}
    producers = {}
    for event in events:
        for gallery in event.gallery_org.all():
            gallerys[gallery] = 1
        for producer in event.producer_org.all():
            producers[producer] = 1
        for festival in event.festival.all():
            festivals[festival] = 1
        for award in event.award.all():
            awards[award] = 1
        for collab in event.collaborator.all():
            collaborators[collab] = 1
        for artist in event.artist.all():
            artists[artist] = 1

    return {'object': object,
			'events': events,
			'festivals': festivals,
			'gallerys': gallerys,
			'awards': awards,
			'collaborators': collaborators,
			'artists': artists,
			'producers': producers,
			'media_url': settings.MEDIA_URL,
			}
register.inclusion_tag('slotechart/print_detail.html')(object_detail)

# ---- seznami ----

def year_list(dater):
    if not dater:
        dater = datetime.date.today().year
    return {'list': ['1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006'],
			'year': datetime.date(int(dater), 1, 1),
			}
register.inclusion_tag('slotechart/print_years.html')(year_list)

def months_list(dater):
    if type(dater) is StringType:
        dater = datetime.date(int(dater), 1, 1)
    months_list = []
    for i in range(12):
        months_list.append(datetime.date(dater.year, (i + 1), 1))
    return {'months_list': months_list,
			'date': dater,
			}
register.inclusion_tag('slotechart/print_months.html')(months_list)

def box_gallerys():
    events = TechArtProject.objects.all()
    orgz = {}
    for event in events:
        for o in event.gallery_org.all():
            orgz[o.id] = o
    return {'object_list': orgz.values() }
register.inclusion_tag('slotechart/object_list.html')(box_gallerys)

def box_orgs():
    events = TechArtProject.objects.filter(producer_org__isnull=False)
    orgz = {}
    for event in events:
        for o in event.producer_org.all():
            orgz[o.id] = o
    for fest in Festival.objects.all():
        for o in fest.producer.all():
            orgz[o.id] = o
	return {'object_list': orgz.values() }
register.inclusion_tag('slotechart/object_list.html')(box_orgs)

# ------

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

    print kwargs
    return kwargs

class BoxListNode(template.Node):
    """
    Example usage:
        {% box_list ObjectName "QuerySet" ["template=foo,order_by=bar,limit=:3"] }
        In third parameter, template, order_by and limit are all optional.

        {% box_list Lend "returned=False,from_who__exact=user.id" "template=box/foo.html,order_by=returned,limit=:2" %}
    """
    def __init__(self, object, queryset, params):
        self.object = object
        self.queryset  = queryset
        self.params = params

    def render(self, context):
        kwargs = parse(self.queryset)
        for i in kwargs:
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
            template_name = "%s/object_list.html" % (model._meta.app_label)

        context['object_list'] = new_queryset
        return template.loader.get_template(template_name).render(context)

def box_list(parser, token):
    bits = token.split_contents()
    object_name = bits[1]
    queryset = bits[2][1:-1]
    if len(bits) > 3:
        params = bits[3][1:-1]
    else:
        params = ''
    m = __import__("intranet.slotechart.models", '','', object_name)
    object = getattr(m, object_name)
    return BoxListNode(object, queryset, params)
register.tag('box_list', box_list)

