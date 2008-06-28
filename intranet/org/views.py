from django.shortcuts import render_to_response, get_object_or_404
from django.db.models.query import Q
from django.forms import FormWrapper
from django import forms
from django import newforms
from django.template import RequestContext, Context
from django.template.defaultfilters import slugify
from django.db.models import signals
from django.dispatch import dispatcher
from django.core import template_loader

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail

from datetime import date, time, timedelta
import datetime
import mx.DateTime
import re

from intranet.org.models import UserProfile, Project, Category
from intranet.org.models import Place, PlaceInternal, Event, Shopping
from intranet.org.models import Task, Diary, Bug, StickyNote, Lend, Resolution, Comment
from intranet.org.models import KbCategory, KB, Tag, Scratchpad
from django.contrib.auth.models import User

month_dict = { 'jan': 1, 'feb': 2, 'mar': 3,
               'apr': 4, 'maj': 5, 'jun': 6,
               'jul': 7, 'avg': 8, 'sep': 9,
            'okt': 10, 'nov': 11, 'dec': 12, }

# ------------------------------------

def index(request):
    today = datetime.date.today()
    nextday = today + datetime.timedelta(days=8)
    return render_to_response('org/index.html',
                              { 'start_date': today,
                                'end_date': nextday,
                                'today': today,
                              },
                              context_instance=RequestContext(request))
index = login_required(index)

def search(request):
    if request.POST:
        query = request.POST.get('term','')

        kategorije = Category.objects.all()
        kb = KB.objects.all()
        users = User.objects.all()
        events = Event.objects.all()

        for term in query.split():
            kb = kb.filter(content__icontains=term)
            kb = kb.filter(title__icontains=term)
            #kb = kb.filter(KbCategory__icontains=term)
        for term in query.split():
            events = events.filter(announce__icontains=term)
            #events = events.filter(category__icontains=term)
        for term in query.split():
            users = users.filter(name__icontains=term)
        for term in query.split():
            kategorije = kategorije.filter(name__icontains=term)

        objects = list(set(events) | set(kb))
        related = []

        return render_to_response('org/search_results.html', {
                                    'object_list': objects,
                                    'search_term': query,
                                })
    else:
        return HttpResponseRedirect("/intranet/")

def lends_by_user(request, username):
    user = User.objects.get(username__exact=username)
    lend_list = Lend.objects.filter(returned__exact=False).filter(from_who__exact=user)
    return render_to_response('org/lend_archive.html',
                              { 'latest': lend_list,
                              },
                              context_instance=RequestContext(request))
lends_by_user = login_required(lends_by_user)

def shopping_by_cost(request, cost):
    list = Shopping.objects.filter(bought__exact=False)
    if int(cost) == 1:
        list = list.filter(cost__lte=1000)
    elif int(cost) == 2:
        list = list.filter(cost__range=(1000, 10000))
    elif int(cost) == 3:
        list = list.filter(cost__range=(10000, 20000))
    elif int(cost) == 4:
        list = list.filter(cost__range=(20000, 50000))
    elif int(cost) == 5:
        list = list.filter(cost__gte=50000)
    else:
        list = []
        print "not found"
    return render_to_response('org/shopping_archive.html',
                              { 'latest': list,
                              },
                              context_instance=RequestContext(request))
shopping_by_cost = login_required(shopping_by_cost)

def shopping_index(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    projects_shop = []
    tasks_shop = []
    for p in projects:
        s = p.shopping_set.filter(bought__exact=False)
        if s.count() > 0:
            p.Shopping = s
            projects_shop.append(p)
    for p in tasks:
        s = p.shopping_set.filter(bought__exact=False)
        if s.count() > 0:
            p.Shopping = s
            tasks_shop.append(p)
    return render_to_response('org/shopping_index.html',
                              { 'projects_shop': projects_shop,
                                'tasks_shop': tasks_shop,
                              },
                              context_instance=RequestContext(request))
shopping_index = login_required(shopping_index)

def shopping_by_user(request, user):
    user = get_object_or_404(User, pk=user)
    lend_list = Shopping.objects.filter(bought__exact=False).filter(author__exact=user)
    return render_to_response('org/shopping_archive.html',
                              { 'latest': lend_list,
                              },
                              context_instance=RequestContext(request))
shopping_by_user = login_required(shopping_by_user)

def shopping_by_project(request, project):
    project = get_object_or_404(Project, pk=project)
    lend_list = Shopping.objects.filter(bought__exact=False).filter(task__exact=project)
    return render_to_response('org/shopping_archive.html',
                              { 'latest': lend_list,
                              },
                              context_instance=RequestContext(request))
shopping_by_project = login_required(shopping_by_project)

def shopping_by_task(request, task):
    task = get_object_or_404(Task, pk=task)
    lend_list = Shopping.objects.filter(bought__exact=False).filter(project__exact=task)
    return render_to_response('org/shopping_archive.html',
                              { 'latest': lend_list,
                              },
                              context_instance=RequestContext(request))
shopping_by_task = login_required(shopping_by_task)

def stats(request):
    return render_to_response('org/stats.html',
                              { 'today': datetime.date.today() },
                              context_instance=RequestContext(request))
stats = login_required(stats)

def text_log(request):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorow = today + datetime.timedelta(days=2)

    dnevniki = Diary.objects.filter(pub_date__range=(yesterday, today))
    reverzi = Lend.objects.filter(returned__exact=False).filter(due_date__lte=(tomorow))
    dogodki = Event.objects.filter(start_date__range=(today, tomorow))
    novo = Event.objects.filter(pub_date__range=(yesterday, today))
    dogodki_vceraj = Event.objects.filter(start_date__range=(yesterday, today))
    scratchpad = Scratchpad.objects.latest()
    return render_to_response('feeds/nightly_report.html',
                              { 'today': today,
                                'dnevniki': dnevniki,
                                'reverzi': reverzi,
                                'dogodki': dogodki,
                                'novo': novo,
                                'dogodki_vceraj': dogodki_vceraj,
                                'scratchpad': scratchpad,
                              },
                              context_instance=RequestContext(request))

# ------------------------------------

def process_cloud_tag(instance):
    ''' distribution algo n tags to b bucket, where b represents
    font size. '''
    entry = instance
    # be sure you save twice the same entry, otherwise it wont update the new tags.
    entry_tag_list = entry.tags.all()
    for tag in entry_tag_list:
        tag.total_ref = tag.entry_set.all().count();
        tag.save()

    tag_list = Tag.objects.all()
    nbr_of_buckets = 8
    base_font_size = 11
    tresholds = []
    max_tag = max(tag_list)
    min_tag = min(tag_list)
    delta = (float(max_tag.total_ref) - float(min_tag.total_ref)) / (float(nbr_of_buckets))
    # set a treshold for all buckets
    for i in range(nbr_of_buckets):
        tresh_value =  float(min_tag.total_ref) + (i+1) * delta
        tresholds.append(tresh_value)
    # set font size for tags (per bucket)
    for tag in tag_list:
        font_set_flag = False
        for bucket in range(nbr_of_buckets):
            if font_set_flag == False:
                if (tag.total_ref <= tresholds[bucket]):
                    tag.font_size = base_font_size + bucket * 2
                    tag.save()
                    font_set_flag = True

# connect signal
#dispatcher.connect(process_cloud_tag, sender = Event, signal = signals.post_save)

##################################################

def box_diary_change (request, id=None):
    diary = get_object_or_404(Diary, pk=id)
    today = datetime.date.today()
    if request.user == diary.author:
        diary.log_formal = "%s \n\nrazsirjeno: %s \n%s" % (diary.log_formal, today, request.POST['log_formal'])
        diary.log_informal = "%s \n\nrazsirjeno: %s \n%s" % (diary.log_informal, today, request.POST['log_informal'])
        diary.save()
    return HttpResponseRedirect('../')
box_diary_change = login_required(box_diary_change)


def box_diary_add(request):
    manipulator = Diary.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()

        new_data['author'] = request.user.id
        new_data['date_date'] = date.today().strftime("%Y-%m-%d")
        new_data['date_time'] = date.today().strftime("%H:%M")
        length = new_data['length']
        if not re.match(r'\d\d\:\d\d', length):
            length = "%s:00" % int(length)
            new_data['length'] = length

        errors = manipulator.get_validation_errors(new_data)

        if not errors:
            manipulator.do_html2python(new_data)
            new_diary = manipulator.save(new_data)
            new_diary.save()
            return HttpResponseRedirect("/intranet/diarys/%i/" % new_diary.id)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/box_error.html',
                             {'form': form, 'template_file': 'org/box_diary.html'},
                             context_instance=RequestContext(request))

##################################################

def box_lend_add(request):
    manipulator = Lend.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()

        new_data['from_who'] = request.user.id
        new_data['from_date'] = date.today().strftime("%Y-%m-%d")

        errors = manipulator.get_validation_errors(new_data)

        if not errors:
            manipulator.do_html2python(new_data)
            new_lend = manipulator.save(new_data)
            return HttpResponseRedirect("/intranet/lends/%i/" % new_lend.id)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/box_error.html',
                             {'form': form, 'template_file': 'org/box_lend.html'},
                             context_instance=RequestContext(request))

##################################################

def box_shopping_add(request):
    manipulator = Shopping.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()

        new_data['author'] = request.user.id

        errors = manipulator.get_validation_errors(new_data)

        if not errors:
            manipulator.do_html2python(new_data)
            new_lend = manipulator.save(new_data)
            return HttpResponseRedirect("/intranet/shopping/%i/" % new_lend.id)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/box_error.html',
                             {'form': form, 'template_file': 'org/box_shopping.html'},
                             context_instance=RequestContext(request))

def shopping_edit(request, event_id):
    try:
        manipulator = Shopping.ChangeManipulator(event_id)
    except Shopping.DoesNotExist:
        raise Http404
    event = manipulator.original_object

    if request.POST:
        new_data = request.POST.copy()

        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)
            return HttpResponseRedirect("/intranet/shopping/%i/" % event.id)

    else:
        errors = {}
        new_data = manipulator.flatten_data()

    form = forms.FormWrapper(manipulator, new_data, errors)

    return render_to_response('org/form_edit_shopping.html',
                             {'form': form,
                             'event': event, },
                              context_instance=RequestContext(request))

# dodaj podatek o obiskovalcih dogodka
def shopping_buy (request, id=None):
    event = get_object_or_404(Shopping, pk=id)
    event.bought = True
    event.save()
    return HttpResponseRedirect('../')
shopping_buy = login_required(shopping_buy)

def shopping_support (request, id=None):
    event = get_object_or_404(Shopping, pk=id)
    if request.has_key('support'):
        event.supporters.add(request.user)
        event.explanation += "\n\n Predlog podprl %s z razlago:\n\n" % (request.user.username) + request['note']
    elif request.has_key('comment'):
        event.explanation += "\n\n %s komentira:\n\n" % (request.user.username) + request['note']
    event.save()
    return HttpResponseRedirect('../')
shopping_support = login_required(shopping_support)

##################################################

def box_bugs_add(request):
    #print request.POST
    if request.POST:
        new_data = request.POST.copy()
        new_data['author'] = request.user.id

        if 'edit' in new_data:
                manipulator = Bug.ChangeManipulator(Bug.objects.get(name=new_data['name']).id)
                #new_bug = 
#                errors = manipulator.get_validation_errors(new_data)
#                new_bug = manipulator.save(new_data)
#                return HttpResponseRedirect("/intranet/bugs/%i/" % new_bug.id)
        else:
            manipulator = Bug.AddManipulator()

        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            #print new_data
            new_bug = manipulator.save(new_data)
            new_bug.mail()
            return HttpResponseRedirect("/intranet/bugs/%i/" % new_bug.id)

    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/box_error.html',
                             {'form': form, 'template_file': 'org/box_bug.html'},
                             context_instance=RequestContext(request))



class CommentBug(newforms.Form):
    text = newforms.CharField(widget=newforms.Textarea)


def view_bug(request, object_id):

    if request.method == 'POST':
        form = CommentBug(request.POST)
        if form.is_valid():
            new_comment = Comment(bug=Bug.objects.get(pk=object_id), text=form.cleaned_data['text'])
            new_comment.save(request)
            return HttpResponseRedirect(request.META['PATH_INFO'])
    else:
        form = CommentBug()

    return list_detail.object_detail(request, 
        object_id = object_id, 
        queryset = Bug.objects.all(), 
        extra_context = { 
            'resolutions': Resolution.objects.all(), 
            'comments': Comment.objects.all(), 
            'comment_form': form.as_p(), 
        })

##################################################

def event_create(request):
    manipulator = Event.AddManipulator()

    if request.POST:
        new_data = request.POST.copy()

        # autosensing if technician is defined
        if new_data['technician']:
            new_data['require_technician'] = True

        # default to first place - should be Kiberpipa
        if not new_data.has_key('place'):
            new_data['place'] = 1 #Place.objects.get(pk=1)
        if not new_data.has_key('place_internal'):
            new_data['place_internal'] = 1 #Place.objects.get(pk=1)
        if not new_data.has_key('category'):
            new_data['category'] = 1 #Category.objects.get(pk=1)

        # black magic for user friendly length input
        if not new_data.has_key('length'):    # default to 2 hours
            new_data['length'] = '02:00:00'
        elif not re.match(r'\d\d\:00:00', new_data['length']):    # or parse full hours
            if int(new_data['length']) < 10:
              new_data['length'] = "0%s:00:00" % int(new_data['length'])
            else:
              new_data['length'] = "%s:00:00" % int(new_data['length'])

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

            return HttpResponseRedirect("/intranet/events/%i/" % new_event.id)

    # da selecti ostanejo taksni, kot so
        if new_data['project']:
          new_data['project_id']= new_data['project']
        if new_data['category']:
          new_data['category_id']= new_data['category']
        if new_data['technician']:
          new_data['technician_id']= new_data['technician']
        if new_data['responsible']:
          new_data['responsible_id'] = new_data['responsible']

    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/form_add_event.html', {'form': form},
                               context_instance=RequestContext(request))

##################################################

def event_edit(request, event_id):
    try:
        manipulator = Event.ChangeManipulator(event_id)
    except Event.DoesNotExist:
        raise Http404

    event = manipulator.original_object

    if request.POST:
        new_data = request.POST.copy()
        if new_data['technician']:
            new_data['require_technician'] = 'on'

        # default to first place - should be Kiberpipa
        if not new_data.has_key('place'):
            new_data['place'] = 1 #Place.objects.get(pk=1)
        if not new_data.has_key('place_internal'):
            new_data['place_internal'] = 1 #Place.objects.get(pk=1)
        if not new_data.has_key('category'):
            new_data['category'] = 1 #Category.objects.get(pk=1)

        # black magic for user friendly length input
        if not new_data.has_key('length'):    # default to 2 hours
            new_data['length'] = '02:00:00'
        elif not re.match(r'\d\d\:00:00', new_data['length']):    # or parse full hours
            if int(new_data['length']) < 10:
              new_data['length'] = "0%s:00:00" % int(new_data['length'])
            else:
              new_data['length'] = "%s:00:00" % int(new_data['length'])

        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)

            return HttpResponseRedirect("/intranet/events/%i/" % event.id)

        # da selecti ostanejo taksni, kot so
        if new_data['project']:
          new_data['project_id']= new_data['project']
        if new_data['category']:
          new_data['category_id']= new_data['category']
        if new_data['technician']:
          new_data['technician_id']= new_data['technician']
        if new_data['responsible']:
          new_data['responsible_id'] = new_data['responsible']


    else:
        errors = {}
        new_data = manipulator.flatten_data()

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/form_edit_event.html',
                             {'form': form,
                             'event': event, },
                              context_instance=RequestContext(request))

# dodaj podatek o obiskovalcih dogodka
def event_count (request, id=None):
    event = get_object_or_404(Event, pk=id)
    event.visitors = int(request.POST['visitors'])
    event.save()
    return HttpResponseRedirect('../')
event_count = login_required(event_count)

##################################################

def lend_back(request, id=None):
    lend = get_object_or_404(Lend, pk=id)
    if not lend.note:
        lend.note = ""
    lend.note += "\n\n---\nvrnitev potrdil %s, %s " % (request.user, datetime.date.today())
    lend.returned = True
    lend.save()
    return HttpResponseRedirect('../')
lend_back = login_required(lend_back)

#def resolve_bug(request, id=None):
#    bug = get_object_or_404(Bug, pk=id)
#    if bug.assign == request.user:
#        #bug.resolved = True
#        bug.save()
#    return HttpResponseRedirect('../')
#resolve_bug = login_required(resolve_bug)

def takeover_bug(request, id=None):
    bug = get_object_or_404(Bug, pk=id)
    bug.assign = request.user
    bug.save()
    return HttpResponseRedirect('../')
takeover_bug = login_required(takeover_bug)

def move_bug(request, id=None):
    bug = get_object_or_404(Bug, pk=id)
    if not bug.note:
        bug.note = ""
    bug.note += "\n\n---\npreusmeril %s k %s z razlago:\n\n %s" % (request.user, request['assign'], request['note'])
    bug.assign = User.objects.get(username__exact=request['assign'])
    bug.save()
    return HttpResponseRedirect('../')
move_bug = login_required(move_bug)

def resolve_bug(request, id=None):
    bug = get_object_or_404(Bug, pk=id)
    bug.resolution = Resolution.objects.get(pk = request.POST['status'])
    bug.save()
    return HttpResponseRedirect('../')

##################################################

def tehniki_monthly(request, year=None, month=None):
    user = request.user
    iso_week = mx.DateTime.now().iso_week[1]
    if month:
        month = mx.DateTime.Date(int(year), int(month_dict[month]), 1).month
    else:
        month = mx.DateTime.now().month
    if year:
        year = mx.DateTime.Date(int(year), int(month), 1).year
    else:
        year = mx.DateTime.now().year

    month_start = mx.DateTime.Date(year, month, 1)
    month_end = month_start + mx.DateTime.DateTimeDelta(month_start.days_in_month)

    month_number = month
    month = Event.objects.filter(start_date__range=(month_start, month_end), require_technician__exact=True).order_by('start_date')
    log_list = Diary.objects.filter(task=2, date__range=(month_start, month_end))

    for e in month:
        try:
            diary = e.diary_set.get()
            e.diary = diary.id
            e.diary_length = diary.length
        except:
            e.diary = 0

        try:
            e.tech = e.technician.username
        except:
            e.tech = 0

    navigation = monthly_navigation (year, month_number)

    return render_to_response('org/tehniki_index.html',
                             {'month':month,
                             'log_list':log_list,
                             'month_number':month_number,
                             'month_name': month_to_string(month_number),
                             'what': 'mesec',
                             'iso_week': iso_week,
                             'year': year,
                             'navigation': navigation,
                             'start_date': month_start,
                             'end_date': month_end,
                             'ure': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                             },
                             context_instance=RequestContext(request)
                             )
tehniki_monthly = login_required(tehniki_monthly)

def monthly_navigation (year=None, month=None):
    month_prev = month - 1
    month_next = month + 1
    year_prev = year
    year_next = year

    if month_prev < 1:
        month_prev = 12
        year_prev = year - 1

    if month_next > 12:
        month_next = 1
        year_next = year + 1

    return {'prev': '%s/%s' % (year_prev, month_to_string(month_prev)),
            'next': '%s/%s' % (year_next, month_to_string(month_next)) }

def month_to_string (month=None):
    for i in month_dict:
        if month_dict[i] == month:
            return i

def weekly_navigation (year=None, week=None, week_start=None, week_end=None):
    week_prev = week - 1
    week_next = week + 1
    year_prev = year
    year_next = year

    if week_prev < 1:
        week_prev = 52
        year_prev = year - 1

    if week_next > 52:
        week_next = 1
        year_next = year + 1

    return {'prev': '%s/%s' % (year_prev, week_prev),
            'next': '%s/%s' % (year_next, week_next) }

def tehniki(request, year=None, week=None):
    user = request.user
    iso_week = mx.DateTime.now().iso_week
    month = mx.DateTime.now().month

    if year:
      year = int(year)
    else:
      year = mx.DateTime.now().year

    if week:
        i = int(week)
    else:
        i = iso_week[1]

    week_start = mx.DateTime.ISO.Week(year, i, 1)
    week_end = mx.DateTime.ISO.Week(year, i, 8)

    week_number = i

    week_now = week_start
    week = Event.objects.filter(start_date__range=(week_start, week_end), require_technician__exact=True).order_by('start_date')
    log_list = Diary.objects.filter(task=2, date__range=(week_start, week_end))

    for e in week:
        try:
            diary = e.diary_set.get()
            e.diary = diary.id
            e.diary_length = diary.length
        except:
            e.diary = 0

        try:
            e.tech = e.technician.username
        except:
            e.tech = 0

    navigation = weekly_navigation (year, week_number, week_start, week_end)

    return render_to_response('org/tehniki_index.html',
                             {'month':week,
                             'log_list':log_list,
                             'month_number':week_number,
                             'month_name': month_to_string(month),
                             'what': 'teden',
                             'iso_week': week_number,
                             'year': year,
                             'navigation': navigation,
                             'start_date': week_start,
                             'end_date': week_end,
                             'ure': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                             },
                             context_instance=RequestContext(request)
                             )
tehniki = login_required(tehniki)

def tehniki_add(request):
    id = request['uniqueSpot']
    if not id:
        return HttpResponseRedirect('../')

    event = Event.objects.get(pk=id)

    p = Diary(      date=event.start_date,
                    event=event,
                    author=request.user,
                    task=Task.objects.get(pk=2),
                    log_formal=request['log_formal'],
                    log_informal=request['log_informal'],
                    length=datetime.time(int(request['length']),0),
                    )
    p.save()

    return HttpResponseRedirect('../')
tehniki_add = login_required(tehniki_add)

def tehniki_take(request, id):
    e = Event.objects.get(pk=id)
    e.technician = request.user
    e.save()

    return HttpResponseRedirect('../../')
tehniki_take = login_required(tehniki_take)

def tehniki_cancel(request, id):
    e = Event.objects.get(pk=id)
    e.technician = None
    e.save()

    return HttpResponseRedirect('../../')
tehniki_take = login_required(tehniki_take)

def tehniki_text_log(request):
    Date = mx.DateTime.Date
    d = mx.DateTime.now()
    c = mx.DateTime.now() - mx.DateTime.oneDay

    f = mx.DateTime.Date(c.year, c.month, c.day)
    g = mx.DateTime.Date(d.year, d.month, d.day)

    log_list = Diary.objects.filter(task__pk=2, date__range=(f, g))

    return render_to_response('org/dezuranje_text_log.html', {'log_list':log_list,})

# ---
def dezurni_monthly(request, year=None, month=None):
    iso_week = mx.DateTime.now().iso_week
# doloci mesec pregledovanja
    if year:
        year = mx.DateTime.Date(int(year), int(month_dict[month]), 1).year
    else:
        year = mx.DateTime.now().year

    if month:
        month = mx.DateTime.Date(int(year), int(month_dict[month]), 1).month
    else:
        month = mx.DateTime.now().month

    month_start = mx.DateTime.Date(year, month, 1)
    month_end = month_start + mx.DateTime.DateTimeDelta(month_start.days_in_month)

    month_prev = month - 1
    month_next = month + 1
    month_number = month

    month_now = month_start
    month = []

    while month_now < month_end:
        dict = {}
        dict['date'] = month_now.strftime('%d.%m. %a')

        dict['dezurni'] = []

        Time = mx.DateTime.Time

        for i in [Time(hours=10), Time(hours=13), Time(hours=16), Time(hours=19)]:
            dezurni_list = Diary.objects.filter(task=1, date__range=(month_now+i, month_now+i+Time(2.59))).order_by('date')
            dezurni_dict = {}
            if dezurni_list:
                dezurni_obj = dezurni_list[0]
                dezurni_dict['name'] = dezurni_obj.author
                dezurni_dict['admin_id'] = dezurni_obj.id
            else:
                dezurni_dict['unique'] = (month_now+i).strftime('%d.%m.%y-%H:%M')
                dezurni_dict['name'] = None
            dict['dezurni'].append(dezurni_dict)

        month.append(dict)
        month_now = month_now + mx.DateTime.oneDay

    log_list = Diary.objects.filter(task=1, date__range=(month_start, month_end)).order_by('-date')

    navigation = monthly_navigation (year, month_number)

    return render_to_response('org/dezuranje_monthly.html',
                                        {'month':month,
                                        'log_list':log_list,
                                        'year': year,
                                        'iso_week': iso_week[1],
                                        'month_name': month_to_string(month),
                                        'navigation':navigation,
                                        'month_number':month_number,
                                        'start_date': month_start,
                                        'end_date': month_end,
                                        },
                              context_instance=RequestContext(request))
dezurni_monthly = login_required(dezurni_monthly)

def dezurni(request, year=None, week=None, month=None):
    iso_week = mx.DateTime.now().iso_week
    month = mx.DateTime.now().month

    if year:
      year = int(year)
    else:
      year = mx.DateTime.now().year

    if week:
        i = int(week)
    else:
        i = iso_week[1]

    week_start = mx.DateTime.ISO.Week(year, i, 1)
    week_end = mx.DateTime.ISO.Week(year, i, 6)

    week_prev = i - 1
    week_next = i + 1
    week_number = i

    week_now = week_start
    week = []

    while week_now < week_end:
        dict = {}
        dict['date'] = week_now.strftime('%d.%m. %a')
        dict['dezurni'] = []

	Time = mx.DateTime.Time

	###od tega datuma naprej velja nov urnik
	if mx.DateTime.Date(2008, 04, 14) <= week_start:
		nov_urnik = 1
		time_list = [Time(11), Time(16)]
	else:
		nov_urnik = 0
		time_list = [Time(10), Time(13), Time(16), Time(19)]
    

        for i in time_list:
            dezurni_list = Diary.objects.filter(task=1, date__range=(week_now+i, week_now+i+Time(2.59))).order_by('date')
            dezurni_dict = {}
            if dezurni_list:
                dezurni_obj = dezurni_list[0]
                dezurni_dict['name'] = dezurni_obj.author
                dezurni_dict['admin_id'] = dezurni_obj.id
            else:
                dezurni_dict['unique'] = (week_now+i).strftime('%d.%m.%y-%H:%M')
                dezurni_dict['name'] = None
            dict['dezurni'].append(dezurni_dict)

        week.append(dict)
        week_now = week_now + mx.DateTime.oneDay

    log_list = Diary.objects.filter(task__pk=1, date__range=(week_start, week_end)).order_by('-date')
    navigation = weekly_navigation (year, week_number, week_start, week_end)
    #print "%s %s" % (week_start, week_end)
    return render_to_response('org/dezuranje_index.html',
                             {'week': week,
                             'iso_week': week_number,
                             'month_name': month_to_string(month),
                             'log_list':log_list,
                             'navigation':navigation,
                             'year': year,
                             'iso_week': week_number,
			     'week_number':week_number,
                             'nov_urnik': nov_urnik,
                             'start_date': week_start,
                             'end_date': week_end,
                             },
                       context_instance=RequestContext(request))
dezurni = login_required(dezurni)

def dezurni_add(request):
    new_data = request.POST.copy()
    if not request.POST or not new_data.has_key('uniqueSpot'):
        return HttpResponseRedirect('../')
   
    d = mx.DateTime.DateTimeFrom(request['uniqueSpot'].__str__())
    datum = datetime.datetime(year=d.year,
                              month=d.month,
                              day=d.day,
                              hour=d.hour,
                              minute=d.minute,
                              second=0,
                              microsecond=0)

    p = Diary(date=datum,
              author=request.user,
              task=Task.objects.get(pk=1),
              log_formal=request['log_formal'],
              log_informal=request['log_informal'],
              length=datetime.time(3,0),)
    p.save()
    return HttpResponseRedirect('../')
dezurni_add = login_required(dezurni_add)

##################################################

def kb_index(request):
    object_list = KbCategory.objects.all()
    return render_to_response('org/kb_index.html',
                              {'object_list':object_list,},
                              context_instance=RequestContext(request))
kb_index = login_required(kb_index)

def kb_cat(request, kbcat):
	##AFAIK se ta funckija klice samo po tem ko shranis stvar v KB
	return HttpResponseRedirect(KB.objects.filter(title=request.POST['title'])[0].get_absolute_url())

kb_cat = login_required(kb_cat)

def kb_article(request, kbcat, article):
    article = get_object_or_404(KB, slug=article)
    return render_to_response('org/kb_article.html',
                              {'article':article,},
                              context_instance=RequestContext(request))
kb_article = login_required(kb_article)



def kb_article_add(request):
    manipulator = KB.AddManipulator()
    if request.POST:
        new_data = request.POST.copy()
        new_data['editor'] = request.user.id
        if not new_data.has_key('slug') and new_data.has_key('title'):
            new_data['slug'] = slugify(new_data['title'])
        errors = manipulator.get_validation_errors(new_data)
        print errors
        if not errors:
            manipulator.do_html2python(new_data)
            new_article = manipulator.save(new_data)
            return HttpResponseRedirect(new_article.get_absolute_url())
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/kb_add.html',
                             {'form': form},
                              context_instance=RequestContext(request))
kb_article_add = login_required(kb_article_add)

def kb_article_edit(request, id):
    manipulator = KB.ChangeManipulator(id)
    kb = manipulator.original_object

    if request.POST:
      new_data = request.POST.copy()
      new_data['editor'] = request.user.id

      if kb.slug:
        new_data['slug'] = kb.slug
      else:
        new_data['slug'] = slugify(new_data['title'])

      errors = manipulator.get_validation_errors(new_data)
      print errors
      if not errors:
          manipulator.do_html2python(new_data)
          new_article = manipulator.save(new_data)
          return HttpResponseRedirect(new_article.get_absolute_url())
    else:
      errors = {}
      new_data = manipulator.flatten_data()

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('org/kb_add.html',
                           {'form': form},
                            context_instance=RequestContext(request))
#kb_article_edit = login_required(kb_article_edit)

def imenik(request):
    addressbook_dict = {
        'queryset': User.objects.filter(is_active__exact=True),
        'template_name': 'org/imenik_list.html',
    }
    return list_detail.object_list(request, **addressbook_dict)
imenik = login_required(imenik)

def timeline_xml(request):
  #diary_list = Diary.objects.filter(task__id__gt=2)
  event_list = Event.objects.all()
  t = template_loader.get_template("org/timeline_xml.html")
  c = Context({'event_list': event_list})
  return HttpResponse(t.render(c), 'application/xml')

def scratchpad_change(request):
    scratchpad = Scratchpad.objects.latest()
    manipulator = Scratchpad.ChangeManipulator(scratchpad.id)
    print request.POST
    if request.POST:
        new_data = request.POST.copy()
        new_data['author'] = request.user.id
        errors = manipulator.get_validation_errors(new_data)
        print errors
        if not errors:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)

    return HttpResponseRedirect("/intranet/")

