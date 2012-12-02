#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cStringIO import StringIO
import csv
import datetime
import logging
import os
import random
import shutil
import string
import subprocess
import tempfile

import mx.DateTime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django_mailman.models import List
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template
from django.utils import simplejson
from django.views.generic import CreateView, UpdateView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView
from PIL import Image

from intranet.org.models import (Project, Email,
    Event, Shopping, Person, Sodelovanje, TipSodelovanja, Diary,
    Lend, Scratchpad)
from intranet.org.forms import (DiaryFilter, AddEventEmails,
    EventForm, LendForm, ShoppingForm, DiaryForm,
    ImageResizeForm, IntranetImageForm,
    NewMemberForm)


month_dict = {'jan': 1, 'feb': 2, 'mar': 3,
    'apr': 4, 'maj': 5, 'jun': 6,
    'jul': 7, 'avg': 8, 'sep': 9,
    'okt': 10, 'nov': 11, 'dec': 12,
}
reverse_month_dict = dict(((i[1], i[0]) for i in month_dict.iteritems()))
logger = logging.getLogger(__name__)


@login_required
def temporary_upload(request):
    """
    Accepts an image upload to server and saves it in a temporary folder.
    """
    if not 'image' in request.FILES:
        return HttpResponse(simplejson.dumps({'status': 'no image uploaded'}))

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
        return HttpResponse(simplejson.dumps({'status': 'couldn\'t open the image'}))

    local_dir = os.path.join(settings.MEDIA_ROOT, 'tmp', request.session.session_key)
    try:
        shutil.rmtree(local_dir, onerror=lambda f, p, e: None)
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
    if request.POST:
        form = ImageResizeForm(request.POST)
        if form.errors:
            return HttpResponse(simplejson.dumps({'status': "%r" % form.errors}))
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
            else:
                return HttpResponse(simplejson.dumps({'status': "%r" % form.errors}))
        else:
            return HttpResponse(simplejson.dumps({'status': 'resized filename and session filename do not match!'}))
    else:
        return HttpResponse(simplejson.dumps({'status': 'only POST requests!'}))


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
    events = events.get_date_events(today - datetime.timedelta(days=14), today)

    # is public and no visitors
    no_visitors = events.filter(public__exact=True).filter(visitors__exact=0)

    # is videoed and no attached video
    no_video = events.needs_video()

    # is pictured and no flicker id
    no_pictures = events.filter(require_photo__exact=True).filter(flickr_set_id__exact=None)

    unfinished_events = (no_visitors, no_video, no_pictures)

    # give us a random rageface!
    # they're under static/org/images/ragaface/
    # i'd list them and do a random that way, but apparantly getting the
    # path to the static dir is quite a chore with a multi-app django
    # deployment
    rageface = random.choice(["angry-unhappy.png", "determined-challenge-accepted.png", "happy-big-smile.png", "happy-cuteness-overload.png", "happy-derpina-eyes-closed.png", "happy-derpina.png", "happy-epic-win.png", "happy-everything-went-better-than-expected.png", "happy-female.png", "happy-i-see-what-you-did-there.png", "happy-kitteh-smile.png", "happy-never-alone.png", "happy-oh-stop-it-you.png", "happy-pfftch.png", "happy-smile-he-he-he.png", "happy-smile.png", "happy-thumbs-up.png", "happy-yes.png", "misc-clean-all-the-things.png", "rage-unhappy.png", "sad-forever-alone-happy.png", "trees-happy-smoking.png", "troll-sincere-troll.png"])

    return render_to_response('org/index.html',
                              {'start_date': today,
                                'end_date': nextday,
                                'today': today,
                                'rageface': rageface,
                                'diary_form': DiaryForm(),
                                'diary_edit': False,
                                'lend_form': LendForm(),
                                'lend_edit': False,
                                'unfinished_events': unfinished_events
                              },
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

    ###od tega datuma naprej velja nov urnik
    Time = mx.DateTime.Time
    if mx.DateTime.Date(2008, 04, 14) <= month_start and mx.DateTime.Date(2008, 9, 14) > month_start:
        nov_urnik = 1
        time_list = [Time(11), Time(16)]
    elif mx.DateTime.Date(2008, 9, 14) <= month_start:
        nov_urnik = 2
        time_list = [Time(10), Time(14), Time(18)]
    else:
        nov_urnik = 0
        time_list = [Time(10), Time(13), Time(16), Time(19)]
    slot_duration = Time(8) if len(time_list) < 2 else time_list[1] - time_list[0]
    logging.debug("SLOT DURATION: %s hours" % slot_duration.hours)

    # load the diary objects for this month
    diarys = Diary.objects.filter(task=22, date__range=(month_start, month_end)).order_by('date')
    d = 0

    # group them in their respective dezuranje slot
    while month_now < month_end:
        day_dict = {}
        day_dict['date'] = month_now.strftime('%d.%m. %a')
        day_dict['slots'] = []

        for slot in time_list:
            slot_range = (month_now + slot, month_now + slot + slot_duration - 0.01)
            logging.debug("CHECKING SLOT [%s, %s]" % (slot_range[0], slot_range[1]))
            diarys_in_slot = []
            slot_dict = {'unique': None, 'diaries': []}

            # find diarys for this particular time slot, if any
            while d < len(diarys) and diarys[d].date <= slot_range[1]:
                #if diarys[d].date >= slot_range[0]:
                logging.debug("Adding diary %s to slot [%s, %s]" % (diarys[d], slot_range[0], slot_range[1]))
                diarys_in_slot.append(diarys[d])
                d += 1

            # todo: there may be multiple diarys per term (multiple dezurni etc)
            if diarys_in_slot:
                for diary in diarys_in_slot:
                    slot_dict['diaries'].append({'author': diary.author, 'id': diary.id})
            else:
                # noone has signed up for this slot yet
                slot_dict['unique'] = (month_now + slot).strftime('%d.%m.%y-%H:%M')

            day_dict['slots'].append(slot_dict)

        month.append(day_dict)
        month_now = month_now + mx.DateTime.oneDay

    navigation = monthly_navigation(year, month_number)

    return render_to_response('org/dezuranje_monthly.html',
                                        {'month': month,
                                        'log_list': diarys,
                                        'year': year,
                                        'iso_week': iso_week[1],
                                        'month_start': month_start,
                                        'month_name': month_to_string(month_number),
                                        'navigation': navigation,
                                        'month_number': month_number,
                                        'start_date': month_start,
                                        'end_date': month_end,
                                        'nov_urnik': nov_urnik,
                                        'time_list': time_list,
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
        date_range = (datetime.datetime(int(year), 1, 1, 0, 0), datetime.datetime(int(year), 12, 31, 23, 59))
    else:
        year = this_year
        date_range = (datetime.datetime(year, 1, 1, 0, 0), today - datetime.timedelta(1))

    # common query
    q = Event.objects.filter(start_date__range=date_range)
    min_year = Event.objects.aggregate(models.Min('pub_date'))['pub_date__min']
    years = range(min_year.year, this_year + 2)

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
                              locals(),
                              context_instance=RequestContext(request))


def commit_hook(request):
    """github post commit hook to log diaryies"""
    if request.META['REMOTE_ADDR'] not in ['207.97.227.253', '50.57.128.197']:
        # see http://help.github.com/post-receive-hooks/
        return HttpResponseForbidden('Request not from github.')

    payload = simplejson.loads(request.POST['payload'])
    diaries = {}

    for commit in payload['commits']:
        first_name, last_name = commit['author']['name'].split()
        user = User.objects.get(models.Q(username=commit['author']['email']) | (models.Q(first_name=first_name) & models.Q(last_name=last_name)))
        commits = diaries.get(user, [])
        commits.append("Commit: %(message)s\n %(url)s" % commit)
        diaries[user] = commits

    for user, text in diaries.iteritems():
        # TODO: if there is a diary for intranet for today, append to that
        diary = Diary(
            log_formal='\n'.join(text),
            author=user,
            length=datetime.time(1),  # 1h
            task=Project.objects.get(id=2),
        )
        diary.save()
    return HttpResponse('OK')




# diary


@login_required
def diarys_form(request, id=None, action=None):
    if id:
        diary_form = DiaryForm(request.POST or None, instance=get_object_or_404(Diary, pk=id))
    else:
        diary_form = DiaryForm(request.POST or None)

    if request.method == "POST" and diary_form.is_valid():
        diary = diary_form.save(commit=False)
        diary.author = request.user
        diary.save()
        return HttpResponseRedirect(reverse('diary_list') + "#diary_%d" % diary.id)

    return render_to_response(
        'org/diary.html',
        {'diary_form': diary_form},
        context_instance=RequestContext(request))


class DetailDiary(DetailView):
    model = Diary

    def get_context_data(self, **kw):
        context = super(DetailDiary, self).get_context_data(**kw)
        context['diary_form'] = DiaryForm(instance=self.model.objects.get(id=self.kwargs['pk']))
        context['diary_edit'] = True
        return context


class ArchiveIndexDiary(ArchiveIndexView):
    date_field = 'date'
    allow_empty = True
    allow_future = True
    paginate_by = 50
    month_format = '%m'

    post = ArchiveIndexView.get

    def get_queryset(self):
        diarys = Diary.objects.all()
        form = DiaryFilter(self.request.POST)
        if self.request.POST and form.is_valid():
            for key, value in form.cleaned_data.items():
                if value:
                    diarys = diarys.filter(**{key: value})

        return diarys.order_by('date')

    def get_context_data(self, **kw):
        context = super(ArchiveIndexDiary, self).get_context_data(**kw)
        context['diary_form'] = DiaryForm(initial=self.request.GET.dict())
        context['filter'] = DiaryFilter(self.request.POST)
        return context


class MixinArchiveDiary(object):
    queryset = Diary.objects.all().order_by('date')
    date_field = 'date'
    allow_empty = True
    allow_future = True
    month_format = '%m'


class YearArchiveDiary(MixinArchiveDiary, YearArchiveView):
    make_object_list = True


class MonthArchiveDiary(MixinArchiveDiary, MonthArchiveView):
    pass


# events


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
def event_edit(request, event_pk=None):
    instance = None
    authors = None

    if event_pk is not None:
        instance = get_object_or_404(Event.objects.select_related(), pk=event_pk)

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

            return redirect('event_list')
            # changed redirect after successful add/edit
            # keeping the old version here just in case we change our mind
            # return HttpResponseRedirect(reverse('intranet.org.views.event_edit', args=[new_event.id]))
        else:
            authors = request.POST.getlist('authors')
    else:
        form = EventForm(instance=instance)

    context = {
        'form': form,
        'tipi': TipSodelovanja.objects.all(),
        'sodelovanja': instance and instance.sodelovanje_set.all() or None,
        'authors': authors,
        # TODO: remove duplicates
        'prev_sodelovanja': Sodelovanje.objects.values('tip__name', 'person__name').distinct().order_by('-person__name'),
        'image': (instance and instance.event_image and instance.event_image.image) or None
        }
    return render_to_response('org/event_edit.html', RequestContext(request, context))

@login_required
def event_diary_edit(request, event_pk):
    diary_id = Diary.objects.filter(event__id=event_pk).filter(author=request.user).all()[0].id
    return DetailDiary.as_view()(request, pk=diary_id)

@login_required
def event_count(request, event_id=None):
    "dodaj podatek o obiskovalcih dogodka"
    event = get_object_or_404(Event, pk=event_id)
    event.visitors = int(request.POST['visitors'])
    event.save()
    return HttpResponseRedirect('/intranet/events/%d/' % event.id)


@login_required
def event_technician_take(request, pk):
    e = Event.objects.get(pk=pk)
    e.technician.add(request.user)
    e.save()
    return redirect('event_list')


@login_required
def event_technician_cancel(request, pk):
    e = Event.objects.get(pk=pk)
    e.technician.remove(request.user)
    e.save()
    return redirect('event_list')


@login_required
def event_officer_take(request, pk):
    e = Event.objects.get(pk=pk)
    e.officers_on_duty.add(request.user)
    e.save()
    return redirect('event_list')


@login_required
def event_officer_cancel(request, pk):
    e = Event.objects.get(pk=pk)
    e.officers_on_duty.remove(request.user)
    e.save()
    return redirect('event_list')


def event_template(request, year=0, week=0):
    """docstring for event_template"""
    week = int(week) or datetime.date.today().isocalendar()[1] + 1
    year = int(year) or datetime.date.today().year

    events = Event.objects.get_week_events(int(year), int(week)).is_public()
    return render_to_response("org/event_template.html", {"events": events}, context_instance=RequestContext(request))


class MixinArchiveEvent(object):
    queryset = Event.objects.load_related_fields().order_by('start_date')
    date_field = 'start_date'
    allow_empty = True
    allow_future = True
    month_format = '%m'

    def get_context_data(self, **kw):
        context = super(MixinArchiveEvent, self).get_context_data(**kw)

        my_diaries = {}
        for diary in Diary.objects.filter(event__in=context['object_list']).filter(author__exact=self.request.user).all():
            my_diaries[diary.event.id] = diary
        context['my_diaries'] = my_diaries
        # TODO: cannot access dictionary by variable in templates
        return context


class YearArchiveEvent(MixinArchiveEvent, YearArchiveView):
    make_object_list = True


class MonthArchiveEvent(MixinArchiveEvent, MonthArchiveView):
    pass


class ArchiveIndexEvent(ArchiveIndexView):
    model = Event
    date_field = 'start_date'
    allow_empty = True
    allow_future = True
    paginate_by = 50

    post = ArchiveIndexView.get

    def get_context_data(self, **kw):
        context = super(ArchiveIndexEvent, self).get_context_data(**kw)
        today = datetime.datetime.today()
        week_number = int(today.strftime('%W'))
        context['events'] = [
            [u'Prejšni teden', Event.objects.get_week_events(today.year, week_number - 1).load_related_fields()],
            [u'Trenutni teden', Event.objects.get_week_events(today.year, week_number).load_related_fields()],
            [u'Naslednji teden', Event.objects.get_week_events(today.year, week_number + 1).load_related_fields()],
            [u'Čez dva tedna', Event.objects.get_week_events(today.year, week_number + 2).load_related_fields()],
        ]
        return context


# shopping


class MixinShopping(object):
    model = Shopping
    form_class = ShoppingForm

    def get_context_data(self, **kw):
        context = super(MixinShopping, self).get_context_data(**kw)
        context['wishes'] = Shopping.objects.filter(bought=False)
        return context

    def form_valid(self, form):
        # TODO: add this to form save method
        shopping = form.save(commit=False)
        shopping.author = self.request.user
        shopping.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('shopping_index'))


class CreateShopping(MixinShopping, CreateView):
    template_name = "org/shopping_index.html"


class UpdateShopping(MixinShopping, UpdateView):
    template_name = "org/shopping_detail.html"


# TODO: this is done with GET requests, which is wrong by all means
# Use POST requests and forms
# Also, rewrite to generic views

@login_required
def shopping_buy(request, id=None):
    event = get_object_or_404(Shopping, pk=id)
    event.bought = True
    event.save()
    return HttpResponseRedirect(reverse('shopping_index'))


@login_required
def shopping_support(request, id=None):
    wish = get_object_or_404(Shopping, pk=id)
    wish.supporters.add(request.user)
    wish.save()
    return HttpResponseRedirect(reverse('shopping_index'))


@login_required
def shopping_responsible(request, id=None):
    wish = get_object_or_404(Shopping, pk=id)
    wish.responsible = request.user
    wish.save()
    return HttpResponseRedirect(reverse('shopping_index'))


# lends


class MixinLend(object):
    model = Lend
    form_class = LendForm

    def get_context_data(self, **kw):
        context = super(MixinLend, self).get_context_data(**kw)
        context['today'] = datetime.date.today()
        context['lends'] = Lend.objects.filter(returned=False).order_by('due_date')
        return context

    def form_valid(self, form):
        new_lend = form.save(commit=False)
        if 'due_date' not in form.cleaned_data:
            # TODO: specify as default on model
            new_lend.due_date = datetime.datetime.today() + datetime.timedelta(7)

        new_lend.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('lend_index'))


class CreateLend(MixinLend, CreateView):
    template_name = "org/lend_index.html"


class UpdateLend(MixinLend, UpdateView):
    template_name = "org/lend_detail.html"


class DetailLend(DetailView):
    model = Lend

    def get_context_data(self, **kw):
        context = super(DetailLend, self).get_context_data(**kw)
        context['lend_form'] = LendForm(instance=self.model.objects.get(id=self.kwargs['pk']))
        context['lend_edit'] = True
        return context


@login_required
def lend_back(request, id=None):  # TODO: this shouldn't be doable with get, make a form
    lend = get_object_or_404(Lend, pk=id)
    if not lend.note:
        lend.note = ""
    # TODO: add this info to DB
    lend.note += "\n\n---\nvrnitev potrdil %s, %s " % (request.user, datetime.date.today())
    lend.returned = True
    lend.save()
    return HttpResponseRedirect(reverse('lend_index'))


@login_required
def add_member(request):
    """Add kiberpipa memeber with all the stuff"""
    if not request.user.is_staff:
        return

    form = NewMemberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # create ldap record
        password = ''.join(random.sample(string.letters + string.digits, 8))

        uid = int(subprocess.Popen("getent passwd | awk -F: '$3 < 3000 { print $3 }' | sort -n | tail -1", stdout=subprocess.PIPE, shell=True).communicate()[0].strip())
        uid += 1
        gid = int(subprocess.Popen("getent group | awk -F: '$3 < 3000 { print $3 }' | sort -n | tail -1", stdout=subprocess.PIPE, shell=True).communicate()[0].strip())
        gid += 1

        ldif_template = get_template('org/member_add.ldif').render(Context(dict(
            data=form.cleaned_data,
            password=password,
            uid=uid,
            gid=gid,
        )))

        with tempfile.NamedTemporaryFile() as f:
            f.write(ldif_template.encode('utf-8'))
            f.flush()
            subprocess.check_call('sudo -u root ldapadd -D cn=admin,dc=kiberpipa,dc=org -f %s -w %s' % (f.name, settings.LDAP_PASSWORD),
                                  shell=True)

        # create home folder
        subprocess.check_call('sudo -u root mkdir -p /home/%s' % form.cleaned_data['username'],
                              shell=True)
        # TODO: chown it (sudoers should be very strict about this)
        #subprocess.check_call('sudo -u root chown -p /home/%s' % form.cleaned_data['username'],
        #                      shell=True)

        # TODO: add member to redmine group

        # add him to pipa-org
        if form.cleaned_data['add_to_private_mailinglist']:
            mailman_list = List.objects.get(id=2)
            try:
                mailman_list.subscribe(form.cleaned_data['email'])
            except:
                pass  # member is already subscribed

        # send email to new user
        html = get_template('mail/member_add_welcome_email.html').render(
            Context(dict(
                username=form.cleaned_data['username'],
                password=password,
        )))
        send_mail(u'Dobrodošel/a v Kiberpipi!',
                  html,
                  settings.DEFAULT_FROM_EMAIL,
                  [form.cleaned_data['email']])

        # add a diary we added a member
        diary = Diary(
            log_formal=u"Dodal novega člana: %s (%s %s)" % (form.cleaned_data['username'],
                                                            form.cleaned_data['firstname'],
                                                            form.cleaned_data['surname']),
            author=request.user,
            length=datetime.time(1),  # 1h
            task=Project.objects.get(id=2),
        )
        diary.save()

        return render_to_response(
            'org/member_add_success.html',
            {'email': form.cleaned_data['email']},
            context_instance=RequestContext(request))

    return render_to_response(
        'org/member_add.html',
        {'form': form},
        context_instance=RequestContext(request))
