from django.shortcuts import render_to_response, get_object_or_404
from django.db.models.query import Q
from django.forms import FormWrapper
from django import forms
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from intranet.kapelica.models import General, Event

from datetime import date, time, timedelta
import datetime
import mx.DateTime
import re

from django.views.generic.date_based import archive_index

def events(*args, **kwargs):
    return archive_index(*args, **kwargs)
events = login_required(events)

def index(request):
    return render_to_response('kapelica/index.html',
                              { 'date': date.today().strftime("%Y-%m-%d") },
                              context_instance=RequestContext(request))
index = login_required(index)

def create_page(request):
    manipulator = General.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            new_event = manipulator.save(new_data)
            return HttpResponseRedirect("/kapelica/pages/%s/" % new_event.slug)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('kapelica/form_add_page.html', {'form': form},
                               context_instance=RequestContext(request))
create_page = login_required(create_page)
##################################################

def edit_page(request, event_id):
    try:
        manipulator = General.ChangeManipulator(event_id)
    except General.DoesNotExist:
        raise Http404
    event = manipulator.original_object

    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)

            return HttpResponseRedirect("/kapelica/pages/%i/" % event.id)
    else:
        errors = {}
        new_data = event.__dict__

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('kapelica/form_edit_page.html',
                             {'form': form, 'event': event},
                              context_instance=RequestContext(request))
edit_page = login_required(edit_page)
###

def create_event(request):
    manipulator = Event.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()

        # default to third place - should be Kapelica
        new_data['place'] = 3 #Place.objects.get(pk=1)

        repeat = int(new_data['event_repeat'])
        rec_freq = int(new_data['event_repeat_freq'])
        rec_type = int(new_data['event_repeat_freq_type'])

        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            new_event = manipulator.save(new_data)
            new_event.save() # to update tags

            # if defined reccurings rules...
            if repeat == 1:
                end_day = new_data['end_date']
                start_day = new_data['start_date_date']
                while end_day > start_day:
                    if rec_type == 0:    # days
                        start_day = start_day + datetime.timedelta(days = rec_freq)
                    elif rec_type == 1:    # weeks
                        start_day = start_day + datetime.timedelta(days = (7 * rec_freq))
                    elif rec_type == 2:    # monts
                        start_day = start_day + datetime.timedelta(months = rec_freq)

                    new_data['start_date_date'] = start_day
                    print "%s -> %s\n" % (start_day, end_day)
                    rec_event = manipulator.save(new_data)
                    rec_event.save() # for tags

            return HttpResponseRedirect("/kapelica/events/%i/" % new_event.id)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('kapelica/form_add_event.html', {'form': form},
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

        # default to third place - should be Kapelica
        new_data['place'] = 3

        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)

            return HttpResponseRedirect("/kapelica/events/%i/" % event.id)
    else:
        errors = {}
        new_data = event.__dict__

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('kapelica/form_edit_event.html',
                             {'form': form, 'event': event},
                              context_instance=RequestContext(request))
edit_event = login_required(edit_event)
