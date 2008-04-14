from django.shortcuts import render_to_response, get_object_or_404
from django.db.models.query import Q
from django.forms import FormWrapper
from django import forms
from django.template import RequestContext
from django.db.models import signals
from django.dispatch import dispatcher

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from datetime import date, time, timedelta
import datetime
import mx.DateTime
import re

from intranet.k4.models import Event
from intranet.org.models import Place
from django.contrib.auth.models import User

from django.views.generic.simple import redirect_to

def index(*args, **kwargs):
    return redirect_to(*args, **kwargs)
index = login_required(index)

def create_event(request):
    manipulator = Event.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()

        # default to second place - should be K4
        new_data['place'] = 2

        repeat = int(new_data['event_repeat'])
        rec_freq = int(new_data['event_repeat_freq'])
        rec_type = int(new_data['event_repeat_freq_type'])

        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            new_event = manipulator.save(new_data)
            new_event.save() # to update tags

            # if defined recurring rules...
            if repeat == 1:
                end_day = new_data['end_date']
                start_day = new_data['start_date_date']
                while end_day > start_day:
                    if rec_type == 0:	# days
                        start_day = start_day + datetime.timedelta(days = rec_freq)
                    elif rec_type == 1:	# weeks
                        start_day = start_day + datetime.timedelta(days = (7 * rec_freq))
                    elif rec_type == 2:	# monts
                        start_day = start_day + datetime.timedelta(months = rec_freq)

                    new_data['start_date_date'] = start_day
                    print "%s -> %s\n" % (start_day, end_day)
                    rec_event = manipulator.save(new_data)
                    rec_event.save() # for tags

            return HttpResponseRedirect("/k4/events/%i/" % new_event.id)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('k4/form_add_event.html', {'form': form},
                               context_instance=RequestContext(request))
create_event = login_required(create_event)

##################################################

def edit_event(request, event_id):
    try:
        manipulator = Event.ChangeManipulator(event_id)
    except Event.DoesNotExist:
        raise Http404
    event = manipulator.original_object

    if request.POST:
        new_data = request.POST.copy()

        # default to second place - should be K4
        new_data['place'] = 2

        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)

            return HttpResponseRedirect("/k4/events/%i/" % event.id)
    else:
        errors = {}
        new_data = event.__dict__

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('k4/form_edit_event.html',
                             {'form': form, 'event': event},
                              context_instance=RequestContext(request))
edit_event = login_required(edit_event)