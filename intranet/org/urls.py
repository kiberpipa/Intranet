import datetime

from django.conf.urls import patterns, url, include
from django.contrib import admin

from intranet.org.models import Event, Diary, Lend, Shopping, Sodelovanje
from intranet.org.feeds import LatestDiarys, LatestEvents
from pipa.ldap.forms import LoginForm


admin.autodiscover()

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=3)
nextday = today + datetime.timedelta(days=8)


prev_week = today - datetime.timedelta(days=7)
this_week = today + datetime.timedelta(days=7)
next_week = this_week + datetime.timedelta(days=7)
next_week2 = next_week + datetime.timedelta(days=7)

event_last = Event.objects.filter(start_date__gte=prev_week, start_date__lt=today).order_by('start_date')
event_this = Event.objects.filter(start_date__gte=today, start_date__lt=this_week).order_by('start_date')
event_next = Event.objects.filter(start_date__gte=this_week, start_date__lt=next_week).order_by('start_date')
event_next2 = Event.objects.filter(start_date__gte=next_week, start_date__lt=next_week2).order_by('start_date')

event_dict = {
    'queryset': Event.objects.all().order_by('-start_date'),
    'date_field': 'start_date',
    'allow_empty': 1,
    'allow_future': 1,
}

event_year = event_dict.copy()
event_year.update({'make_object_list': True})

event_month = event_dict.copy()
months = []
for i in range(1, 13):
    months.append(datetime.datetime(2008, i, 1))

event_month.update({'month_format': '%m',
    'extra_context': {'months': months}})

event_index = {
    'queryset': Event.objects.filter(start_date__gte=today).order_by('start_date'),
    'date_field': 'start_date',
    'allow_empty': 1,
    'allow_future': 1,
    'num_latest': 50,
    'template_name': 'org/event_archive.html',
    'extra_context': {
        'event_last': event_last, 'event_this': event_this,
        'event_next': event_next,
        'event_next2': event_next2,
        'years': range(2006, datetime.date.today().year + 1)
    },
}

event_year = {
    'queryset': Event.objects.all().order_by('start_date'),
    'date_field': 'start_date',
    'allow_empty': 1,
    'allow_future': 1,
    'make_object_list': 1,
}

diary_dict = {
    'queryset': Diary.objects.all().order_by('date'),
    'date_field': 'date',
    'allow_empty': 1,
    'month_format': '%m',
}

diary_year = {
    'queryset': Diary.objects.all().order_by('date'),
    'date_field': 'date',
    'allow_empty': 1,
    'allow_future': 1,
    'make_object_list': 1,
}

lend_dict = {
    'queryset': Lend.objects.all().order_by('due_date'),
    'date_field': 'from_date',
    'allow_empty': 1,
    'extra_context': {
        'responsible': Lend.objects.filter(returned=False).distinct(),
    }
}

sodelovanje_dict = {
    'queryset': Sodelovanje.objects.all(),
    'date_field': '',
    'allow_empty': 1,
}

shopping_dict = {
    'queryset': Shopping.objects.filter(bought__exact=False).order_by('chg_date'),
    'date_field': 'chg_date',
    'allow_empty': 1,
}

sodelovanje_detail = {
    'queryset': Sodelovanje.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'intranet.org.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ldappass/', 'pipa.ldap.views.password_change', name='ldap_password_change'),

    url(r'^events/$', 'intranet.org.views.events', name="event_list"),
    url(r'^events/create/', 'intranet.org.views.event_edit', name="event_create"),
    url(r'^events/(?P<event_id>\d+)/$', 'intranet.org.views.event', name="event_detail"),
    url(r'^events/(?P<event_pk>\d+)/edit/$', 'intranet.org.views.event_edit', name="event_edit"),
    url(r'^events/(?P<event_id>\d+)/count/$', 'intranet.org.views.event_count'),
    url(r'^events/(?P<event_id>\d+)/emails/$', 'intranet.org.views.add_event_emails'),
    url(r'^events/(?P<event>\d+)/info.txt/$', 'intranet.org.views.info_txt'),
    url(r'^events/(?P<event>\d+)/sablona/$', 'intranet.org.views.sablona'),
    url(r'events/pr/(?P<year>\d{4})/(?P<week>\d{1,2})/$', 'intranet.org.views.event_template'),
    url(r'events/pr/$', 'intranet.org.views.event_template'),

    (r'^diarys/$', 'intranet.org.views.diarys'),
    (r'^diarys/(?P<id>\d+)?/?(?P<action>(add|edit))/$', 'intranet.org.views.diarys_form'),
    (r'^diarys/(?P<object_id>\d+)/$', 'intranet.org.views.diary_detail'),

    (r'^shopping/$', 'intranet.org.views.shopping_index'),
    (r'^shopping/cost/(?P<cost>\d+)/$', 'intranet.org.views.shopping_by_cost'),
    (r'^shopping/task/(?P<task>\d+)/$', 'intranet.org.views.shopping_by_task'),
    (r'^shopping/user/(?P<user>\d+)/$', 'intranet.org.views.shopping_by_user'),
    (r'^shopping/proj/(?P<project>\d+)/$', 'intranet.org.views.shopping_by_project'),
    (r'^shopping/(?P<object_id>\d+)/$', 'intranet.org.views.shopping_detail'),
    (r'^shopping/(?P<id>\d+)?/?(?P<action>(add|edit))/(edit/)?$', 'intranet.org.views.shoppings_form'),
    (r'^shopping/(?P<id>\d+)/buy/$', 'intranet.org.views.shopping_buy'),
    (r'^shopping/(?P<id>\d+)/support/$', 'intranet.org.views.shopping_support'),

    (r'^lends/$', 'intranet.org.views.lends'),
    (r'^lends/(?P<id>\d+)?/?(?P<action>(add|edit))/(edit/)?$', 'intranet.org.views.lends_form'),
    (r'^lends/(?P<id>\d+)/back/$', 'intranet.org.views.lend_back'),
    (r'^lends/(?P<object_id>\d+)/$', 'intranet.org.views.lend_detail'),
    (r'^lends/(?P<username>\w+)/$', 'intranet.org.views.lends_by_user'),

    ##sodelovanja
    (r'^sodelovanja/$', 'intranet.org.views.sodelovanja'),
    #(r'^sodelovanja/(?P<object_id>\d+)', 'django.views.generic.list_detail.object_detail', sodelovanje_detail),
    (r'^sodelovanja/person/$', 'intranet.org.views.person'),

    (r'^tmp_upload/', 'intranet.org.views.temporary_upload'),
    (r'^image_crop_tool/resize/', 'intranet.org.views.image_resize'),
    (r'^image_crop_tool/save/', 'intranet.org.views.image_save'),
    (r'^image_crop_tool/$', 'intranet.org.views.image_crop_tool'),

    url(r'^tehniki/$', 'intranet.org.views.tehniki', name="technician_list"),
    (r'^tehniki/(?P<year>\d+)/(?P<month>[a-z]{3})/$', 'intranet.org.views.tehniki_monthly'),
    (r'^tehniki/(?P<year>\d+)/(?P<week>\d+)/$', 'intranet.org.views.tehniki'),
    (r'^tehniki/add/$', 'intranet.org.views.tehniki_add'),
    (r'^tehniki/add/(\d+)/$', 'intranet.org.views.tehniki_take'),
    (r'^tehniki/cancel/(\d+)/$', 'intranet.org.views.tehniki_cancel'),

    (r'^dezurni/$', 'intranet.org.views.dezurni'),
    (r'^dezurni/add/$', 'intranet.org.views.dezurni_add'),
    (r'^dezurni/(?P<year>\d+)/(?P<month>[a-z]{3})/$', 'intranet.org.views.dezurni_monthly'),
    (r'^dezurni/(?P<year>\d+)/(?P<week>\d+)/$', 'intranet.org.views.dezurni'),

    (r'^addressbook/$', 'pipa.addressbook.views.addressbook'),
    (r'^mercenaries/', include('pipa.mercenaries.urls')),
    url(r'^statistika/(?P<year>\d{4})?', 'intranet.org.views.year_statistics', name='statistics_by_year'),

    (r'^wiki/$', 'django.views.generic.simple.redirect_to', {'url': 'https://wiki.kiberpipa.org/'}),

    (r'^autocomplete/person/$', 'intranet.org.views.person_autocomplete'),
    (r'^autocomplete/active_user/$', 'intranet.org.views.active_user_autocomplete'),

    #scratchpad
    (r'^scratchpad/change/$', 'intranet.org.views.scratchpad_change'),

    #accounts
    url(r'^accounts/login/$', 'pipa.ldap.views.login', {'authentication_form': LoginForm}, name="account_login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="account_logout"),
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/intranet/admin'}),

    #rss
    (r'^feeds/$', 'django.views.generic.simple.direct_to_template', {'template': 'org/feeds_index.html'}),
    (r'^feeds/diarys/', LatestDiarys()),
    (r'^feeds/events/', LatestEvents()),

    #timelines
    (r'^timelines/$', 'django.views.generic.simple.direct_to_template', {'template': 'org/timeline.html'}),
)

urlpatterns += patterns('django.views.generic.date_based',
    (r'events/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', event_dict),
    (r'events/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3}|[0-9]{1,2})/$', 'archive_month', event_month),
    url(r'events/arhiv/(?P<year>\d{4})/$', 'archive_year', event_year, name="event_arhive_year"),

    (r'diarys/arhiv/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/$', 'archive_day', diary_dict),
    (r'diarys/arhiv/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_month', diary_dict),
    (r'diarys/arhiv/(?P<year>\d{4})/$', 'archive_year', diary_year),
)
