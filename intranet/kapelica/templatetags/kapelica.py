from django.template import Context, Library, RequestContext
#from django import template
#from django import forms
#from django.forms import FormWrapper
#from django.template import resolve_variable

#from intranet import k6_4
#from intranet import org
#from intranet import k4
#from intranet import kapelica

import datetime

register = Library()

def print_event(form):
	return {'event': form }
register.inclusion_tag('kapelica/print_event.html')(print_event)

def form_event(form):
	return {'form': form }
register.inclusion_tag('kapelica/form_event.html')(form_event)

def box_reccurings(form):
    return {'form': form }
register.inclusion_tag('kapelica/box_reccurings.html')(box_reccurings)
