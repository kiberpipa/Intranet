#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import re
import csv
from cStringIO import StringIO

import mx.DateTime
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import list_detail, date_based
from django.utils import simplejson
from django.db import models
from PIL import Image

from pipa.video.utils import prepare_video_zip
from intranet.org.models import (Project, Email,
    Event, Shopping, Person, Sodelovanje, TipSodelovanja, Task, Diary,
    Lend, Scratchpad)
from intranet.org.forms import (DiaryFilter, PersonForm, AddEventEmails,
    EventForm, SodelovanjeFilter, LendForm, ShoppingForm, DiaryForm,
    ImageResizeForm, IntranetImageForm)


month_dict = {'jan': 1, 'feb': 2, 'mar': 3,
    'apr': 4, 'maj': 5, 'jun': 6,
    'jul': 7, 'avg': 8, 'sep': 9,
    'okt': 10, 'nov': 11, 'dec': 12,
}
reverse_month_dict = dict(((i[1], i[0]) for i in month_dict.iteritems()))


@login_required
def temporary_upload(request):
    """
    Accepts an image upload to server and saves it in a temporary folder.
    """
    if not 'image' in request.FILES:
        return HttpResponse(simplejson.dumps({'status': 'fail'}))

    filename = request.FILES['image']._get_name().strip().lower()
    imgdata = StringIO(request.FILES['image'].read())
    imgdata.seek(0)
    # check that it's image
    if not (filename.endswith('.jpg') or filename.endswith('.jpeg')):
        return HttpResponse(simplejson.dumps({'status': '.jpeg only!'}))

    try:
        im = Image.open(imgdata)
        im.size
    except Exception:
        return HttpResponse(simplejson.dumps({'status': 'fail'}))

    local_dir = os.path.join(settings.MEDIA_ROOT, 'tmp', request.session.session_key)
    try:
        os.makedirs(local_dir)
    except IOError:
        pass
    local_filename = os.path.join(local_dir, filename)
    url = os.path.join(settings.MEDIA_URL, 'tmp', request.session.session_key, filename)

    f = open(local_filename, 'wb')
    f.write(imgdata.getvalue())
    f.close()

    request.session['temporary_filename'] = local_filename
    ret = simplejson.dumps({'status': 'ok', 'link': url, 'filename': local_filename})
    return HttpResponse(ret)


@login_required
def image_resize(request):
    if not request.POST:
        return HttpResponse(simplejson.dumps({'status': 'fail1'}))
    else:
        form = ImageResizeForm(request.POST)
        if form.errors:
            return HttpResponse(simplejson.dumps({'status': 'fail2'}))
        else:
            if form.cleaned_data.get('filename') != request.session.get('temporary_filename'):
                return HttpResponse(simplejson.dumps({'status': 'fail3'}))
            else:
                # resize!
                x1, x2, y1, y2 = tuple(form.cleaned_data['resize'])
                box = (int(x1), int(y1), int(x2) - 1, int(y2) - 1)

                resized_dir = os.path.join(settings.MEDIA_ROOT, 'tmp', request.session.session_key, 's')
                try:
                    if not os.path.exists(resized_dir):
                        os.makedirs(resized_dir)
                except Exception:
                    return HttpResponse(simplejson.dumps({'status': 'fail4'}))
                resized_filename = os.path.join(resized_dir, os.path.basename(form.cleaned_data.get('filename')))
                image_filename = form.cleaned_data['filename']
                im = Image.open(image_filename)
                cropped = im.crop(box)
                index = cropped.resize((250, 130), Image.ANTIALIAS)
                index.save(resized_filename)
                request.session['resized_filename'] = resized_filename
                resized_url = os.path.join(settings.MEDIA_URL, 'tmp', request.session.session_key, 's', os.path.basename(form.cleaned_data.get('filename')))
                return HttpResponse(simplejson.dumps({'status': 'ok',
                    'resized_url': resized_url,
                    'resized_filename': resized_filename}))

    return HttpResponse(simplejson.dumps({'status': 'ok'}))


@login_required
def image_save(request):
    if request.method == 'POST':
        if request.POST.get('resized_filename') == request.session.get('resized_filename'):
            from django.utils.datastructures import MultiValueDict
            # ok, save the image
            thumb_filename = request.session.get('resized_filename')
            uploaded_file = SimpleUploadedFile(name=os.path.basename(thumb_filename), content=open(thumb_filename, 'rb').read())
            files = MultiValueDict()
            files['image'] = uploaded_file
            form = IntranetImageForm(request.POST, files=files)
            if not form.errors:
                image = form.save()
                return HttpResponse(simplejson.dumps({'status': 'ok', 'image_id': image.id}))
    return HttpResponse(simplejson.dumps({'status': 'fail'}))


@login_required
def image_crop_tool(request):
    form = ImageResizeForm()
    context = {'form': form}
    return render_to_response("org/image_crop_tool.html", RequestContext(request, context))


@login_required
def index(request):
    today = datetime.datetime.today()
    nextday = today + datetime.timedelta(days=8)

    events = Event.objects.all()

    # 1. events that are newer or equal may pass
    # 2. events that are older or equal may pass
    events = events.get_date_events(today - datetime.timedelta(days=14), start_date__lte=today)

    # is public and no visitors
    no_visitors = events.filter(public__exact=True).filter(visitors__exact=0)

    # is videoed and no attached video
    no_video = events.needs_video()

    # is pictured and no flicker id
    no_pictures = events.filter(require_photo__exact=True).filter(flickr_set_id__exact=None)

    unfinished_events = (no_visitors, no_video, no_pictures)

    return render_to_response('org/index.html',
                              {'start_date': today,
                                'end_date': nextday,
                                'today': today,
                                'diary_form': DiaryForm(),
                                'diary_edit': False,
                                'lend_form': LendForm(),
                                'lend_edit': False,
                                'unfinished_events': unfinished_events
                              },
                              context_instance=RequestContext(request))


@login_required
def lend_back(request, id=None):
    lend = get_object_or_404(Lend, pk=id)
    if not lend.note:
        lend.note = ""
    lend.note += "\n\n---\nvrnitev potrdil %s, %s " % (request.user, datetime.date.today())
    lend.returned = True
    lend.save()
    return HttpResponseRedirect('../')


@login_required
def lends(request):
    if request.method == 'POST':
        form = LendForm(request.POST)
        if form.is_valid():
            new_lend = form.save()
            if 'due_date' not in form.cleaned_data:
                new_lend.due_date = datetime.datetime.today() + datetime.timedelta(7)

            return HttpResponseRedirect(new_lend.get_absolute_url())
    else:
        form = LendForm()

    return date_based.archive_index(request,
        queryset=Lend.objects.all().order_by('due_date'),
        date_field='from_date',
        allow_empty=1,
        extra_context={
            'form': form,
        },
    )


@login_required
def lends_form(request, id=None, action=None):
    #process the add/edit requests, redirect to full url if successful, display form with errors if not.
    if request.method == 'POST':
        if id:
            lend_form = LendForm(request.POST, instance=Lend.objects.get(id=id))
        else:
            lend_form = LendForm(request.POST)

        if lend_form.is_valid():
            lend = lend_form.save()
            return HttpResponseRedirect(lend.get_absolute_url())
    else:
        if id:
            lend_form = LendForm(instance=Lend.objects.get(id=id))
        else:
            lend_form = LendForm()

    return render_to_response('org/lend.html', {
        'lend_form': lend_form,
        'lend_edit': True,
        }, context_instance=RequestContext(request)
    )


@login_required
def lend_detail(request, object_id):
    return list_detail.object_detail(request,
        object_id=object_id,
        queryset=Lend.objects.all(),
        extra_context={
            'lend_form': LendForm(instance=Lend.objects.get(id=object_id)),
            'lend_edit': True,
        })


@login_required
def lends_by_user(request, username):
    responsible = []
    for l in Lend.objects.filter(returned=False):
        if l.from_who not in responsible:
            responsible.append(l.from_who)
    user = User.objects.get(username__exact=username)
    lend_list = Lend.objects.filter(returned__exact=False).filter(from_who__exact=user)
    return render_to_response('org/lend_archive.html',
                              {'latest': lend_list,
                                'responsible': responsible,
                              },
                              context_instance=RequestContext(request))


@login_required
def shoppings_form(request, id=None, action=None):
    #process the add/edit requests, redirect to full url if successful, display form with errors if not.
    if request.method == 'POST':
        if id:
            shopping_form = ShoppingForm(request.POST, instance=Shopping.objects.get(pk=id))
        else:
            shopping_form = ShoppingForm(request.POST)

        if shopping_form.is_valid():
            shopping = shopping_form.save(commit=False)
            shopping.author = request.user
            shopping.save()
            return HttpResponseRedirect(shopping.get_absolute_url())
    else:
        if id:
            shopping_form = ShoppingForm(instance=shopping.objects.get(id=id))
        else:
            shopping_form = ShoppingForm()

    return render_to_response('org/shopping.html', {
        'shopping_form': shopping_form,
        'shopping_edit': True,
        }, context_instance=RequestContext(request)
    )


@login_required
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
    return render_to_response('org/shopping_archive.html',
                              {'latest': list},
                              context_instance=RequestContext(request))


@login_required
def shopping_index(request):
    wishes = Shopping.objects.filter(bought=False)
    return render_to_response('org/shopping_index.html',
                              {'wishes': wishes,
                              'shopping_form': ShoppingForm(),
                              'shopping_edit': False,
                              },
                              context_instance=RequestContext(request))


@login_required
def shopping_by_user(request, user):
    user = get_object_or_404(User, pk=user)
    lend_list = Shopping.objects.filter(bought__exact=False).filter(author__exact=user)
    return render_to_response('org/shopping_archive.html', {'latest': lend_list, },
                              context_instance=RequestContext(request))


@login_required
def shopping_by_project(request, project):
    project = get_object_or_404(Project, pk=project)
    lend_list = Shopping.objects.filter(bought__exact=False).filter(task__exact=project)
    return render_to_response('org/shopping_archive.html',
                              {'latest': lend_list, },
                              context_instance=RequestContext(request))


@login_required
def shopping_by_task(request, task):
    task = get_object_or_404(Task, pk=task)
    lend_list = Shopping.objects.filter(bought__exact=False).filter(project__exact=task)
    return render_to_response('org/shopping_archive.html',
                              {'latest': lend_list, },
                              context_instance=RequestContext(request))


@login_required
def stats(request):
    return render_to_response('org/stats.html',
                              {'today': datetime.date.today()},
                              context_instance=RequestContext(request))


@login_required
def diarys_form(request, id=None, action=None):
    if request.method == 'POST':
        if id:
            diary_form = DiaryForm(request.POST, instance=Diary.objects.get(id=id))
        else:
            diary_form = DiaryForm(request.POST)

        if diary_form.is_valid():
            diary = diary_form.save(commit=False)
            diary.author = request.user
            diary.save()
            return HttpResponseRedirect(diary.get_absolute_url())
    else:
        if id:
            diary_form = DiaryForm(instance=Diary.objects.get(id=id))
        else:
            diary_form = DiaryForm()

    return render_to_response('org/diary.html', {
        'diary_form': diary_form,
        'diary_edit': True,
        }, context_instance=RequestContext(request)
    )


@login_required
def diarys(request):
    diarys = Diary.objects.all()
    if request.POST:
        filter = DiaryFilter(request.POST)
        if filter.is_valid():
            for key, value in filter.cleaned_data.items():
                if value:
                    ##'**' rabis zato da ti python resolva spremenljivke (as opposed da passa dobesedni string)
                    diarys = diarys.filter(**{key: value})
    else:
        filter = DiaryFilter()

    return date_based.archive_index(request,
        queryset=diarys.order_by('date'),
        date_field='date',
        allow_empty=1,
        extra_context={
            'filter': filter,
            'diary_form': DiaryForm(),
        }
    )


@login_required
def diary_detail(request, object_id):
    return list_detail.object_detail(request,
        object_id=object_id,
        queryset=Diary.objects.all(),
        extra_context={
            #the next line is the reason for wrapper function, dunno how to
            #pass generic view dynamic form.
            'diary_form': DiaryForm(instance=Diary.objects.get(id=object_id)),
            'diary_edit': True,
        })


# dodaj podatek o obiskovalcih dogodka
@login_required
def shopping_buy(request, id=None):
    event = get_object_or_404(Shopping, pk=id)
    event.bought = True
    event.save()
    return HttpResponseRedirect('../')


@login_required
def shopping_support(request, id=None):
    wish = get_object_or_404(Shopping, pk=id)
    wish.supporters.add(request.user)
    wish.save()
    return HttpResponseRedirect(wish.get_absolute_url())


@login_required
def shopping_detail(request, object_id):
    return list_detail.object_detail(request,
        object_id=object_id,
        queryset=Shopping.objects.all(),
        extra_context={
            #the next line is the reason for wrapper function, dunno how to
            #pass generic view dynamic form.
            'shopping_form': ShoppingForm(instance=Shopping.objects.get(id=object_id)),
            'shopping_edit': True,
        })


@login_required
def person_autocomplete(request):
    hits = []
    if 'q' in request.GET:
        hits = ['%s\n' % i for i in Person.objects.filter(name__icontains=request.GET['q'])]
    return HttpResponse(''.join(hits), mimetype='text/plain')


@login_required
def active_user_autocomplete(request):
    hits = []
    if 'q' in request.GET:
        hits = ['%s\n' % i for i in User.objects.filter(is_active=True).order_by('username').filter(username__icontains=request.GET['q'])]
    return HttpResponse(''.join(hits), mimetype='text/plain')


@login_required
def events(request):
    today = datetime.datetime.today()
    week_number = int(today.strftime('%W'))

    return date_based.archive_index(request,
        queryset=Event.objects.all(),
        date_field='start_date',
        allow_empty=1,
        extra_context={
            'event_last': Event.objects.get_week_events(today.year, week_number - 1),
            'event_this': Event.objects.get_week_events(today.year, week_number),
            'event_next': Event.objects.get_week_events(today.year, week_number + 1),
            'event_next2': Event.objects.get_week_events(today.year, week_number + 2),
            'years': range(2006, today.year + 1),
        },
    )


@login_required
def add_event_emails(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        form = AddEventEmails(request.POST)
        if form.is_valid():
            for e in form.cleaned_data['emails'].split('\n'):
                email = Email.objects.get_or_create(email=e.strip())[0]
                if email not in event.emails.all():
                    event.emails.add(email)
        event.save()
    return HttpResponseRedirect(event.get_absolute_url())


@login_required
def info_txt(request, event):
    event = get_object_or_404(Event, pk=event)
    content = []
    if event.sodelovanje_set.all():
        content.append(u'author: %s' % u', '.join([s.person.name for s in event.sodelovanje_set.all()]))
    content.append(u'title: %s' % event.title)
    content.append(u'date: %s' % event.start_date.strftime('%d.%m.%Y'))
    content.append(u'cat: %s' % event.project)
    desc = event.announce
    desc = re.sub('\s+', ' ', re.sub('<.*?>', '', desc))
    content.append(u'desc: %s' % (desc,))
    content.append(u'url: http://www.kiberpipa.org%s' % event.get_public_url())
    content.append(u'intranet-id: %s' % event.id)
    response = HttpResponse(mimetype='application/octet-stream')
    response['Content-Disposition'] = "attachment; filename=info.txt"
    content_str = u'\n'.join(content)
    response.write(content_str.encode('utf-8'))
    return response


@login_required
def sablona(request, event):
    event = get_object_or_404(Event, pk=event)
    person = u', '.join([i.person.name for i in event.sodelovanje_set.all() if i.tip.id in (1, 5)]),
    return prepare_video_zip(event.slug, event.title, event.start_date, person)


@login_required
def event_edit(request, event_pk=None):
    instance = None
    if event_pk is not None:
        instance = Event.objects.get(pk=event_pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)

        authors = [a.split(' - ') for a in request.POST.getlist('authors') if ' - ' in a]

        if form.is_valid():
            new_event = form.save(commit=False)
            old_sodelovanja = set()
            if instance is not None:
                old_sodelovanja = set(instance.sodelovanje_set.all())

            sodelovanja = set()
            for author, tip in authors:
                tip = TipSodelovanja.objects.get(name=tip)
                # ensure the Person actually exists
                try:
                    person = Person.objects.get(name=author)
                except Person.DoesNotExist:
                    person = Person(name=author)
                    person.save()

                try:
                    s = Sodelovanje.objects.get(event=new_event, tip=tip, person=person)
                except Sodelovanje.DoesNotExist:
                    s = Sodelovanje(event=new_event, tip=tip, person=person)
                    s.save()
                sodelovanja.add(s)
            new_event.save()
            # somehow this causes event.technician to become empty??
            #form.save_m2m()

            # remove old objects, that were not POSTed
            for i in old_sodelovanja & sodelovanja ^ old_sodelovanja:
                i.delete()

            return HttpResponseRedirect(new_event.get_absolute_url())
    else:
        form = EventForm(instance=instance)

    context = {
        'form': form,
        'tipi': TipSodelovanja.objects.all(),
        'sodelovanja': instance and instance.sodelovanje_set.all() or None,
        # TODO: remove duplicates
        'prev_sodelovanja': Sodelovanje.objects.all(),
        'image': (instance and instance.event_image and instance.event_image.image) or None
        }
    return render_to_response('org/event_edit.html', RequestContext(request, context))


@login_required
def event(request, event_id):
    return list_detail.object_detail(request,
        queryset=Event.objects.all(),
        object_id=event_id,
        extra_context={
            'sodelovanja': Sodelovanje.objects.filter(event=event_id),
            'emails_form': AddEventEmails(),
        }
    )


@login_required
def event_count(request, event_id=None):
    "dodaj podatek o obiskovalcih dogodka"
    event = get_object_or_404(Event, pk=event_id)
    event.visitors = int(request.POST['visitors'])
    event.save()
    return HttpResponseRedirect('/intranet/events/%d/' % event.id)


@login_required
def person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = Person(name=form.cleaned_data['name'])
            person.save()
            for key, value in form.cleaned_data.items():
                if not value or key == 'name':
                    continue

                clas = key[0].capitalize() + key[1:]
                exec 'from intranet.org.models import ' + clas
                for k in request.POST.getlist(key):
                    new_var = locals()[clas](**{key: k})
                    new_var.save()
                    Person.__dict__[key].__get__(person, clas).add(new_var)

    return HttpResponseRedirect('../')


@login_required
def sodelovanja(request):
    sodelovanja = Sodelovanje.objects.all()
    person_form = PersonForm()
    if request.method == 'POST':
        form = SodelovanjeFilter(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                ##'**' rabis zato da ti python resolva spremenljivke (as opposed da passa dobesedni string)
                if value and key != 'export':
                    sodelovanja = sodelovanja.filter(**{key: value})

    else:
        form = SodelovanjeFilter()

    try:
        export = form.cleaned_data['export']
        if export:
            from reportlab.pdfgen.canvas import Canvas
            output = StringIO()
            if export == 'txt':
                for i in sodelovanja:
                    output.write("%s\n" % i)
            elif export == 'pdf':
                pdf = Canvas(output)
                rhyme = pdf.beginText(30, 200)
                for i in sodelovanja:
                    rhyme.textLine(i.__unicode__())
                pdf.drawText(rhyme)
                pdf.showPage()
                pdf.save()
            elif export == 'csv':
                for i in sodelovanja:
                    output.write("%s\n" % i)

            response = HttpResponse(mimetype='application/octet-stream')
            response['Content-Disposition'] = "attachment; filename=" + 'export.' + export
            response.write(output.getvalue())
            return response

    except AttributeError:
        pass

    return render_to_response('org/sodelovanja.html',
        {'sodelovanja': sodelovanja, 'form': form,
        'admin_org': '%s/intranet/admin/org/' % settings.BASE_URL,
        'person_form': person_form},
        context_instance=RequestContext(request))


def monthly_navigation(year=None, month=None):
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
            'next': '%s/%s' % (year_next, month_to_string(month_next))}


def month_to_string(month=None):
    for i in month_dict:
        if month_dict[i] == month:
            return i


def weekly_navigation(year=None, week=None, week_start=None, week_end=None):
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
            'next': '%s/%s' % (year_next, week_next)}


@login_required
def tehniki_monthly(request, year=None, month=None):
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
    events = Event.objects.get_date_events(month_start, month_end).filter(require_technician__exact=True)
    log_list = Diary.objects.filter(task=23, date__range=(month_start, month_end))

    month = []
    for e in events:
        try:
            diary = e.diary_set.get()
            e.diary = diary.id
            e.diary_length = diary.length
        except:
            e.diary = 0

        month.append((set(), e))

    navigation = monthly_navigation(year, month_number)

    return render_to_response('org/technicians_index.html', {
         'month': month,
         'log_list': log_list,
         'month_number': month_number,
         'month_name': month_to_string(month_number),
         'what': 'mesec',
         'iso_week': iso_week,
         'year': year,
         'navigation': navigation,
         'start_date': month_start,
         'end_date': month_end,
         'ure': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
     }, context_instance=RequestContext(request))


@login_required
def tehniki(request, year=None, week=None):
    iso_week = mx.DateTime.now().iso_week

    year = int(year or mx.DateTime.now().year)
    week_number = int(week or iso_week[1])

    week_start = mx.DateTime.ISO.Week(year, week_number, 1)
    week_end = mx.DateTime.ISO.Week(year, week_number, 8)
    month_number = week_start.month

    events = Event.objects.filter(start_date__range=(week_start, week_end), require_technician__exact=True).order_by('start_date')
    log_list = Diary.objects.filter(task=23, date__range=(week_start, week_end))

    week = []
    for e in events:
        authors = [a.author for a in e.diary_set.all()]
        non_diary = set(e.technician.all()) - set(authors)
        #(<array of authors of diarys>, event)
        week += [(non_diary, e)]

    navigation = weekly_navigation(year, week_number, week_start, week_end)

    return render_to_response('org/technicians_index.html', {
        'month': week,
         'log_list': log_list,
         'month_number': week_number,
         'month_name': reverse_month_dict[month_number],
         'what': 'teden',
         'iso_week': week_number,
         'year': year,
         'navigation': navigation,
         'start_date': week_start,
         'end_date': week_end,
         'ure': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
     }, context_instance=RequestContext(request))


@login_required
def tehniki_add(request):
    id = request.POST['uniqueSpot']
    if not id:
        return HttpResponseRedirect('../')

    event = Event.objects.get(pk=id)

    p = Diary(
        date=event.start_date,
        event=event,
        author=request.user,
        task=Project.objects.get(pk=23),
        log_formal=request.POST['log_formal'],
        log_informal=request.POST['log_informal'],
        length=datetime.time(int(request.POST.get('length', 1)), 0),
    )
    p.save()

    return HttpResponseRedirect('../')


@login_required
def tehniki_take(request, id):
    e = Event.objects.get(pk=id)
    e.technician.add(request.user)
    e.save()
    return redirect('technician_list')


@login_required
def tehniki_cancel(request, id):
    e = Event.objects.get(pk=id)
    e.technician.remove(request.user)
    e.save()
    return HttpResponseRedirect('../../')


@login_required
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
    month_number = month
    month_now = month_start
    month = []

    while month_now < month_end:
        dict = {}
        dict['date'] = month_now.strftime('%d.%m. %a')
        dict['dezurni'] = []

        Time = mx.DateTime.Time

        for i in [Time(hours=10), Time(hours=14), Time(hours=18)]:
            dezurni_list = Diary.objects.filter(task=22, date__range=(month_now + i, month_now + i + Time(3.59))).order_by('date')
            dezurni_dict = {}
            if dezurni_list:
                dezurni_obj = dezurni_list[0]
                dezurni_dict['name'] = dezurni_obj.author
                dezurni_dict['admin_id'] = dezurni_obj.id
            else:
                dezurni_dict['unique'] = (month_now + i).strftime('%d.%m.%y-%H:%M')
                dezurni_dict['name'] = None
            dict['dezurni'].append(dezurni_dict)

        month.append(dict)
        month_now = month_now + mx.DateTime.oneDay

    log_list = Diary.objects.filter(task=22, date__range=(month_start, month_end)).order_by('-date')

    navigation = monthly_navigation(year, month_number)

    return render_to_response('org/dezuranje_monthly.html',
                                        {'month': month,
                                        'log_list': log_list,
                                        'year': year,
                                        'iso_week': iso_week[1],
                                        'month_name': month_to_string(month),
                                        'navigation': navigation,
                                        'month_number': month_number,
                                        'start_date': month_start,
                                        'end_date': month_end,
                                        },
                              context_instance=RequestContext(request))


@login_required
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
    week_number = i
    week_now = week_start
    week = []

    while week_now < week_end:
        dict = {}
        dict['date'] = week_now.strftime('%d.%m. %a')
        dict['dezurni'] = []

        Time = mx.DateTime.Time

        ###od tega datuma naprej velja nov urnik
        if mx.DateTime.Date(2008, 04, 14) <= week_start and mx.DateTime.Date(2008, 9, 14) > week_start:
            nov_urnik = 1
            time_list = [Time(11), Time(16)]
        elif mx.DateTime.Date(2008, 9, 14) <= week_start:
            nov_urnik = 2
            time_list = [Time(10), Time(14), Time(18)]
        else:
            nov_urnik = 0
            time_list = [Time(10), Time(13), Time(16), Time(19)]

        for i in time_list:
            dezurni_list = Diary.objects.filter(task=22, date__range=(week_now + i, week_now + i + Time(2.59))).order_by('date')
            dezurni_dict = {}
            if dezurni_list:
                dezurni_obj = dezurni_list[0]
                dezurni_dict['name'] = dezurni_obj.author
                dezurni_dict['admin_id'] = dezurni_obj.id
            else:
                dezurni_dict['unique'] = (week_now + i).strftime('%d.%m.%y-%H:%M')
                dezurni_dict['name'] = None
            dict['dezurni'].append(dezurni_dict)

        week.append(dict)
        week_now = week_now + mx.DateTime.oneDay

    log_list = Diary.objects.filter(task__pk=22, date__range=(week_start, week_end)).order_by('-date')
    navigation = weekly_navigation(year, week_number, week_start, week_end)
    return render_to_response('org/dezuranje_index.html',
                             {'week': week,
                             'iso_week': week_number,
                             'month_name': month_to_string(month),
                             'log_list': log_list,
                             'navigation': navigation,
                             'year': year,
                             'iso_week': week_number,
                             'week_number': week_number,
                             'nov_urnik': nov_urnik,
                             'start_date': week_start,
                             'end_date': week_end,
                             },
                       context_instance=RequestContext(request))


@login_required
def dezurni_add(request):
    new_data = request.POST.copy()
    if not request.POST or not 'uniqueSpot' in new_data:
        return HttpResponseRedirect('../')

    d = mx.DateTime.DateTimeFrom(request.POST['uniqueSpot'].__str__())
    datum = datetime.datetime(year=d.year,
                              month=d.month,
                              day=d.day,
                              hour=d.hour,
                              minute=d.minute,
                              second=0,
                              microsecond=0)

    p = Diary(date=datum,
              author=request.user,
              task=Project.objects.get(pk=22),
              log_formal=request.POST['log_formal'],
              log_informal=request.POST['log_informal'],)
    p.save()
    return HttpResponseRedirect('../')


@login_required
def scratchpad_change(request):
    if request.POST:
        try:
            scratchpad = Scratchpad.objects.latest('id')
        except Scratchpad.DoesNotExist:
            scratchpad = Scratchpad()
        scratchpad.author = request.user
        scratchpad.content = request.POST['content']
        scratchpad.save()
    return HttpResponseRedirect("/intranet/")


@login_required
def year_statistics(request, year=None):
    """Most common statistics from database,
    aggregated nicely and with some csv output.
    """
    today = datetime.date.today()
    this_year = today.year
    if year:
        date_range = (datetime.datetime(year, 1, 1, 0, 0), datetime.datetime(year, 12, 31, 23, 59))
    else:
        year = this_year
        date_range = (datetime.datetime(year, 1, 1, 0, 0), today - datetime.timedelta(1))

    # common query
    q = Event.objects.filter(start_date__range=date_range)
    min_year = Event.objects.aggregate(models.Min('pub_date'))['pub_date__min']
    years = range(min_year.year, this_year + 1)

    # TODO: Project manager
    by_project_events = Project.objects.filter(event__start_date__range=date_range)\
        .values('name')\
        .annotate(num_events=models.Count('event'), num_visitors=models.Sum('event__visitors'))

    # TODO: make this one big query that is customizable through html forms
    # TODO: https://github.com/joshourisman/django-tablib
    csv_file = request.GET.get('csv', None)
    if csv_file:
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % csv_file
        writer = csv.writer(response)

        if csv_file == 'javni_dogodki':
            public_events = q.filter(public=True).order_by('start_date').values_list("title", "visitors", "start_date").all()
            writer.writerow(['Naslov', u'Število obiskovalcev'.encode('utf-8'), u'Začetek dogodka'.encode('utf-8')])
            for row in public_events:
                writer.writerow([unicode(r).encode('utf-8') for r in row])

        if csv_file == 'izpis_dogodkov_z_udelezenci':
            all_events = q.extra(select={
                'event_id': "org_event.id",
                'date_nohour': "date_trunc('day', start_date)::date",
                'people': "SELECT textcat_all(org_person.name) FROM org_sodelovanje, org_person WHERE org_event.id=event_id AND org_sodelovanje.person_id=org_person.id"
            }).values_list('title', 'visitors', 'people', 'date_nohour')
            writer.writerow(['Naslov', u'Število obiskovalcev'.encode('utf-8'), u'Sodelovanja', u'Začetek dogodka'.encode('utf-8')])
            for row in all_events:
                writer.writerow([unicode(r).encode('utf-8') for r in row])
        return response

    return render_to_response('org/statistics_year.html',
        locals(), context_instance=RequestContext(request))


def event_template(request, year=None, week=None):
    """docstring for event_template"""
    week = week or datetime.date.today().isocalendar()[1]
    year = year or datetime.date.today().year

    events = Event.objects.get_week_events(int(year), int(week + 1))
    return render_to_response("org/event_template.html", {"events": events}, context_instance=RequestContext(request))
