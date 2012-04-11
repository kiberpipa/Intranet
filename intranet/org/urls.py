from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView

from intranet.org.feeds import LatestDiarys, LatestEvents
from intranet.org.views import (DetailLend, DetailDiary, DetailShopping,
                                DetailEvent, ArchiveIndexEvent,
                                ArchiveIndexLend, ArchiveIndexDiary,
                                MonthArchiveEvent, YearArchiveEvent,
                                MonthArchiveDiary, YearArchiveDiary)
from pipa.ldap.forms import LoginForm


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'intranet.org.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ldappass/', 'pipa.ldap.views.password_change', name='ldap_password_change'),

    url(r'^events/$', login_required(ArchiveIndexEvent.as_view()), name="event_list"),
    url(r'^events/arhiv/(?P<year>\d{4})/$', login_required(YearArchiveEvent.as_view()), name="event_arhive_year"),
    url(r'^events/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3}|[0-9]{1,2})/$', login_required(MonthArchiveEvent.as_view())),
    url(r'^events/create/', 'intranet.org.views.event_edit', name="event_create"),
    url(r'^events/(?P<pk>\d+)/$', login_required(DetailEvent.as_view()), name="event_private_detail"),
    url(r'^events/(?P<event_pk>\d+)/edit/$', 'intranet.org.views.event_edit', name="event_edit"),
    url(r'^events/(?P<event_id>\d+)/count/$', 'intranet.org.views.event_count'),
    url(r'^events/(?P<event_id>\d+)/emails/$', 'intranet.org.views.add_event_emails'),
    url(r'^events/(?P<event>\d+)/info.txt/$', 'intranet.org.views.info_txt'),
    url(r'^events/(?P<event>\d+)/sablona/$', 'intranet.org.views.sablona'),
    url(r'^events/pr/(?P<year>\d{4})/(?P<week>\d{1,2})/$', 'intranet.org.views.event_template'),
    url(r'^events/pr/$', 'intranet.org.views.event_template'),

    (r'^diarys/$', login_required(ArchiveIndexDiary.as_view())),
    (r'^diarys/arhiv/(?P<year>\d{4})/$', login_required(YearArchiveDiary.as_view())),
    (r'^diarys/arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3}|[0-9]{1,2})/$', login_required(MonthArchiveDiary.as_view())),
    (r'^diarys/(?P<id>\d+)?/?(?P<action>(add|edit))/$', 'intranet.org.views.diarys_form'),
    (r'^diarys/(?P<pk>\d+)/$', login_required(DetailDiary.as_view())),

    (r'^shopping/$', 'intranet.org.views.shopping_index'),
    (r'^shopping/cost/(?P<cost>\d+)/$', 'intranet.org.views.shopping_by_cost'),
    (r'^shopping/task/(?P<task>\d+)/$', 'intranet.org.views.shopping_by_task'),
    (r'^shopping/user/(?P<user>\d+)/$', 'intranet.org.views.shopping_by_user'),
    (r'^shopping/proj/(?P<project>\d+)/$', 'intranet.org.views.shopping_by_project'),
    (r'^shopping/(?P<pk>\d+)/$', login_required(DetailShopping.as_view())),
    (r'^shopping/(?P<id>\d+)?/?(?P<action>(add|edit))/(edit/)?$', 'intranet.org.views.shoppings_form'),
    (r'^shopping/(?P<id>\d+)/buy/$', 'intranet.org.views.shopping_buy'),
    (r'^shopping/(?P<id>\d+)/support/$', 'intranet.org.views.shopping_support'),

    (r'^lends/$', login_required(ArchiveIndexLend.as_view())),
    (r'^lends/(?P<id>\d+)?/?(?P<action>(add|edit))/(edit/)?$', 'intranet.org.views.lends_form'),
    (r'^lends/(?P<id>\d+)/back/$', 'intranet.org.views.lend_back'),
    (r'^lends/(?P<pk>\d+)/$', login_required(DetailLend.as_view())),
    (r'^lends/(?P<username>\w+)/$', 'intranet.org.views.lends_by_user'),

    (r'^sodelovanja/$', 'intranet.org.views.sodelovanja'),
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

    (r'^scratchpad/change/$', 'intranet.org.views.scratchpad_change'),
    url(r'^statistika/(?P<year>\d{4})?', 'intranet.org.views.year_statistics', name='statistics_by_year'),
    (r'^autocomplete/person/$', 'intranet.org.views.person_autocomplete'),
    (r'^autocomplete/active_user/$', 'intranet.org.views.active_user_autocomplete'),

    # rss
    (r'^feeds/$', TemplateView.as_view(template_name='org/feeds_index.html')),
    (r'^feeds/diarys/', LatestDiarys()),
    (r'^feeds/events/', LatestEvents()),

    (r'^addressbook/$', 'pipa.addressbook.views.addressbook'),
    (r'^mercenaries/', include('pipa.mercenaries.urls')),
    url(r'^accounts/login/$', 'pipa.ldap.views.login', {'authentication_form': LoginForm}, name="account_login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="account_logout"),
    (r'^wiki/$', RedirectView.as_view(url='https://wiki.kiberpipa.org/')),
)
