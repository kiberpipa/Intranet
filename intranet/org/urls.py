from django.conf.urls.defaults import *
from intranet.org.models import Event, Bug, Diary, Lend, Shopping, Resolution, Comment, Sodelovanje
from intranet.org.feeds import LatestBugs, LatestDiarys, BugsByUser, ToDo, LatestEvents
from django.contrib.auth.models import User

#from django.contrib import databrowse
#databrowse.site.register(Diary)
#databrowse.site.register(Event)

import datetime


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=3)
nextday = today + datetime.timedelta(days=8)


prev_week = today - datetime.timedelta(days=7)
this_week = today + datetime.timedelta(days=7)
next_week = this_week + datetime.timedelta(days=7)
next_week2 = next_week + datetime.timedelta(days=7)

event_last =  Event.objects.filter(start_date__gte=prev_week, start_date__lt=today).order_by('start_date')
event_this =  Event.objects.filter(start_date__gte=today, start_date__lt=this_week).order_by('start_date')
event_next =  Event.objects.filter(start_date__gte=this_week, start_date__lt=next_week).order_by('start_date')
event_next2 =  Event.objects.filter(start_date__gte=next_week, start_date__lt=next_week2).order_by('start_date')



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
for i in range(1,13):
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
    'extra_context': {'event_last': event_last, 'event_this': event_this,
		'event_next': event_next, 'event_next2': event_next2, 'years': range (2006, datetime.date.today().year+1)},
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
}

addressbook_dict = {
    'queryset': User.objects.filter(is_active=True).order_by('username'),
    'template_name': 'org/imenik_list.html',
}

diary_year = {
    'queryset': Diary.objects.all().order_by('date'),
    'date_field': 'date',
    'allow_empty': 1,
    'allow_future': 1,
    'make_object_list': 1,
}

bug_dict = {
    'queryset': Bug.objects.all().order_by('chg_date'),
    'date_field': 'pub_date',
    'allow_empty': 1,
}

responsible = []
for l in Lend.objects.filter(returned=False):
    if l.from_who not in responsible:
        responsible.append(l.from_who)

lend_dict = {
    'queryset': Lend.objects.all().order_by('due_date'),
    'date_field': 'from_date',
    'allow_empty': 1,
    'extra_context': {
        'responsible': responsible,
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

bug_extra = {
}

sodelovanje_detail = {
    'queryset': Sodelovanje.objects.all(),
}

feeds = {
    'bugs': LatestBugs,
    'diarys': LatestDiarys,
    'userbugs': BugsByUser,
    'todos': ToDo,
    'events': LatestEvents,
}

urlpatterns = patterns('',
    (r'^search/$', 'intranet.org.views.search'),
    (r'^$', 'intranet.org.views.index'),
    (r'^stats/$', 'intranet.org.views.stats'),
    (r'^stats/text_log/$', 'intranet.org.views.text_log'),

#    (r'events/$',    'django.views.generic.list_detail.object_list', event_list),
    (r'^events/create/', 'intranet.org.views.nf_event_create'),
    (r'^events/(?P<event>\d+)/edit/$', 'intranet.org.views.nf_event_edit'),
    (r'^events/(\d+)/count/$', 'intranet.org.views.event_count'),
    (r'^events/$',    'intranet.org.views.events'),
    (r'^events/(?P<object_id>\d+)/$', 'intranet.org.views.event'),

    #(r'^diarys/(?P<task>\w+)/$', 'intranet.org.views.diarys_by_task'),
    (r'^diarys/(?P<id>\d+)?/?(?P<action>(add|edit))/(edit/)?$', 'intranet.org.views.diarys_form'),
    (r'^diarys/(?P<object_id>\d+)/$', 'intranet.org.views.diary_detail'),
    (r'^diarys/?$',    'intranet.org.views.diarys'),

    (r'^shopping/$', 'intranet.org.views.shopping_index'),
    (r'^shopping/(?P<id>\d+)?/?(?P<action>(add|edit))/(edit/)?$', 'intranet.org.views.shoppings_form'),
    (r'^shopping/(?P<object_id>\d+)/$', 'intranet.org.views.shopping_detail'),
    (r'^shopping/cost/(?P<cost>\d+)/$', 'intranet.org.views.shopping_by_cost'),
    (r'^shopping/task/(?P<task>\d+)/$', 'intranet.org.views.shopping_by_task'),
    (r'^shopping/user/(?P<user>\d+)/$', 'intranet.org.views.shopping_by_user'),
    (r'^shopping/proj/(?P<project>\d+)/$', 'intranet.org.views.shopping_by_project'),
    (r'^shopping/(?P<id>\d+)/buy/$', 'intranet.org.views.shopping_buy'),
    (r'^shopping/(?P<id>\d+)/support/$', 'intranet.org.views.shopping_support'),

    (r'^lends/(?P<id>\d+)?/?(?P<action>(add|edit))/(edit/)?$', 'intranet.org.views.lends_form'),
    (r'^lends/(?P<object_id>\d+)/$', 'intranet.org.views.lend_detail'),
    (r'^lends/(?P<id>\d+)/back/$', 'intranet.org.views.lend_back'),
    (r'^lends/(?P<username>\w+)/$', 'intranet.org.views.lends_by_user'),
    (r'lends/?$',    'intranet.org.views.lends'),

    ##bugs
    #mali wraper okoli generic viewa da lahko procesiramo komentar 
    #(r'^bugs/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', bug_detail),
    (r'^bugs/(?P<object_id>\d+)/$', 'intranet.org.views.view_bug'),
    (r'^bugs/add/$', 'intranet.org.views.add_bug'),
    (r'^bugs/(?P<id>\d+)/resolve/$', 'intranet.org.views.resolve_bug'),

    ##issues, obsolotes bugs
    (r'bugs/?$',    'intranet.org.views.issues'),
    (r'bugs/(?P<bug_id>\d+)/comment/$',    'intranet.org.views.comment_add'),
    (r'bugs/(?P<bug_id>\d+)/edit/$',    'intranet.org.views.bug_edit'),
    (r'bugs/(?P<bug_id>\d+)/subtask/$',    'intranet.org.views.bug_subtask'),

    ##sodelovanja
    (r'^sodelovanja/$', 'intranet.org.views.sodelovanja'),
    #(r'^sodelovanja/(?P<object_id>\d+)', 'django.views.generic.list_detail.object_detail', sodelovanje_detail),
    (r'^sodelovanja/person/$', 'intranet.org.views.person'),


    (r'^mercenaries/(?P<year>\d+)?/?(?P<month>\d+)?/?$', 'intranet.org.views.mercenaries'),
    #(r'^mercenaries/(<?P<id>\d+)/placa$', 'intranet.org.views.mercenary_salary'),
    (r'^mercenaries/(?P<year>\d+)?/?(?P<month>\d+)?/?(?P<id>\d+|vsi|compact)/placa/$', 'intranet.org.views.mercenary_salary'),

    (r'^clipping/add/', 'intranet.org.views.clipping_add'),
    (r'^clipping/', 'intranet.org.views.clipping'),

    (r'^tehniki/(?P<year>\d+)/(?P<month>[a-z]{3})/$', 'intranet.org.views.tehniki_monthly'),
    (r'^tehniki/(?P<year>\d+)/(?P<week>\d+)/$', 'intranet.org.views.tehniki'),
    (r'^tehniki/$', 'intranet.org.views.tehniki'),
    (r'^tehniki/add/$', 'intranet.org.views.tehniki_add'),
    (r'^tehniki/add/(\d+)/$', 'intranet.org.views.tehniki_take'),
    (r'^tehniki/cancel/(\d+)/$', 'intranet.org.views.tehniki_cancel'),

    (r'^dezurni/(?P<year>\d+)/(?P<month>[a-z]{3})/$', 'intranet.org.views.dezurni_monthly'),
    (r'^dezurni/(?P<year>\d+)/(?P<week>\d+)/$', 'intranet.org.views.dezurni'),
    (r'^dezurni/add/$', 'intranet.org.views.dezurni_add'),
    (r'^dezurni/$', 'intranet.org.views.dezurni'),

    (r'^kb/(?P<kbcat>[-\w]+)/(?P<article>[-\w]+)', 'intranet.org.views.kb_article'),
    (r'^kb/$', 'intranet.org.views.kb_index'),

    (r'^imenik/$', 'intranet.org.views.imenik'),


    (r'^autocomplete/(?P<search>[^/]*)$', 'intranet.org.views.autocomplete'),

    #scratchpad
    (r'^scratchpad/change/$', 'intranet.org.views.scratchpad_change'),

    #accounts
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/intranet/admin'}),
    (r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': 'login/'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    #(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'accounts/login/'}),

    #rss
    (r'^feeds/$', 'django.views.generic.simple.direct_to_template', {'template': 'org/feeds_index.html'}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

#timelines

urlpatterns += patterns('',
    (r'^timelines/source.xml$', 'intranet.org.views.timeline_xml'),
    (r'^timelines/$', 'django.views.generic.simple.direct_to_template', {'template': 'org/timeline.html'}),
)

urlpatterns += patterns('django.views.generic.date_based',
    (r'events/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',    'archive_day',   event_dict),
    (r'events/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3}|[0-9]{1,2})/$',    'archive_month', event_month),
    (r'events/arhiv/(?P<year>\d{4})/$',    'archive_year', event_year),
    #(r'events/$',    'archive_index', event_index),
    #(r'events/$',    'archive_index', event_index),
#    (r'events/$',    'archive_year', event_index),

    (r'diarys/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',    'archive_day',   diary_dict),
    (r'diarys/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',    'archive_month', diary_dict),
    (r'diarys/arhiv/(?P<year>\d{4})/$',    'archive_year',  diary_year),
    #(r'diarys/?$',    'archive_index', diary_dict),

    #(r'bugs/?$',    'archive_index', bug_dict),
    #(r'lends/?$',    'archive_index', lend_dict),
#    (r'shopping/?$',    'archive_index', shopping_dict),
)
