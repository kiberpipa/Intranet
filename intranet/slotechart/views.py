from django.shortcuts import render_to_response, get_object_or_404
from django.db.models.query import Q
from django.forms import FormWrapper
from django import forms
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from intranet.slotechart.models import TechArtProject, Festival

##################################################

def producers_list(request):
    events = TechArtProject.objects.filter(producer_org__isnull=False)
    orgz = {}
    for event in events:
        for o in event.producer_org.all():
            orgz[o.id] = o
    for fest in Festival.objects.all():
        for o in fest.producer.all():
            orgz[o.id] = o
    return render_to_response('slotechart/seznami.html',
                              {'object_list': orgz.values(),
                               'what': 'Producenti',
                               'menu': 'producenti'},
                               context_instance=RequestContext(request))

def gallery_list(request):
    events = TechArtProject.objects.all()
    orgz = {}
    for event in events:
        for o in event.gallery_org.all():
            orgz[o.id] = o
    return render_to_response('slotechart/seznami.html',
                             {'object_list': orgz.values(),
                              'what': 'Galerije',
                              'menu': 'galerije'},
                               context_instance=RequestContext(request))

##################################################


def create_event(request):
    manipulator = TechArtProject.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            new_event = manipulator.save(new_data)
            return HttpResponseRedirect("/slotechart/projects/%i/" % new_event.id)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('slotechart/form_add_event.html', {'form': form},
                               context_instance=RequestContext(request))
create_event = login_required(create_event)

def edit_event(request, event_id):
    try:
        manipulator = TechArtProject.ChangeManipulator(event_id)
    except TechArtProject.DoesNotExist:
        raise Http404
    event = manipulator.original_object

    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)

            return HttpResponseRedirect("/slotechart/projects/%i/" % event.id)
    else:
        errors = {}
        new_data = event.__dict__

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('slotechart/form_edit_event.html',
                             {'form': form, 'event': event},
                              context_instance=RequestContext(request))
edit_event = login_required(edit_event)
