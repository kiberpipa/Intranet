from django.conf.urls.defaults import *
from intranet.slotechart.models import TechArtProject, Artist, Award, Festival, Organisation

event_dict = {
    'queryset': TechArtProject.objects.all(),
    'date_field': 'start_date',
    'allow_empty': 1,
    'extra_context': {'what': 'projekti', 'menu': 'archive'},
}
event_year = {
    'queryset': TechArtProject.objects.all(),
    'date_field': 'start_date',
    'allow_empty': 1,
    'make_object_list': 1,
    'extra_context': {'what': 'projekti', 'menu': 'archive'},
}
event_detail = {
    'queryset': TechArtProject.objects.all(),
    'extra_context': {'what': 'projekt', 'menu': 'archive'},
}

artists_list = {
    'queryset': Artist.objects.all(),
    'allow_empty': 1,
    'template_name': 'slotechart/seznami.html',
    'extra_context': {'what': 'Avtorji', 'menu': 'avtorji'},
}
awards_list = {
    'queryset': Award.objects.all(),
    'allow_empty': 1,
    'template_name': 'slotechart/seznami.html',
    'extra_context': {'what': 'Nagrade', 'menu': 'nagrade'},
}
producers_list = {
    'queryset': Organisation.objects.all(),
    'allow_empty': 1,
    'template_name': 'slotechart/seznami.html',
    'extra_context': {'what': 'Producenti', 'menu': 'producenti'},
}
gallerys_list = {
    'queryset': Organisation.objects.all(),
    'allow_empty': 1,
    'template_name': 'slotechart/seznami.html',
    'extra_context': {'what': 'Galerije', 'menu': 'galerije'},
}
fests_list = {
    'queryset': Festival.objects.all(),
    'allow_empty': 1,
    'template_name': 'slotechart/seznami.html',
    'extra_context': {'what': 'Festivali', 'menu': 'festivali'},
}
artists_detail = {
    'queryset': Artist.objects.all(),
    'extra_context': {'what': 'Avtor', 'menu': 'avtorji'},
}
awards_detail = {
    'queryset': Award.objects.all(),
    'extra_context': {'what': 'Nagrada', 'menu': 'nagrade'},
}
producers_detail = {
    'queryset': Organisation.objects.all(),
    'extra_context': {'what': 'Producent', 'menu': 'producenti'},
}
gallerys_detail = {
    'queryset': Organisation.objects.all(),
    'template_name': 'slotechart/gallery_detail.html',
    'extra_context': {'what': 'Galerija', 'menu': 'galerije'},
}
fests_detail = {
    'queryset': Festival.objects.all(),
    'extra_context': {'what': 'Festival', 'menu': 'festivali'},
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'slotechart/index.html' }),

    (r'^projects/create/', 'intranet.slotechart.views.create_event'),
    (r'^projects/(\d+)/edit/$', 'intranet.slotechart.views.edit_event'),
    (r'^projects/(\d+)/count/$', 'intranet.slotechart.views.count_event'),
    (r'^projects/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', event_detail),

    (r'^kb/edit/(?P<id>\d+)', 'intranet.slotechart.views.kb_article_edit'),
    (r'^kb/(?P<kbcat>\w+)/(?P<article>\w+)', 'intranet.slotechart.views.kb_article'),
    (r'^kb/add/$', 'intranet.slotechart.views.kb_article_add'),
    (r'^kb/(?P<kbcat>\w+)', 'intranet.slotechart.views.kb_cat'),
    (r'^kb/$', 'intranet.slotechart.views.kb_index'),

    (r'^producenti/$', 'intranet.slotechart.views.producers_list'),
    (r'^galerije/$', 'intranet.slotechart.views.gallery_list'),
)

urlpatterns += patterns('django.views.generic.date_based',
    (r'arhiv/(?P<year>\d{4})/$',	'archive_year',  event_year),
    (r'arhiv/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',	'archive_month',  event_dict),
    (r'arhiv/$',	'archive_index', event_dict),
)

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^umetniki/$', 'object_list', artists_list),
    (r'^festivali/$', 'object_list', fests_list),
    (r'^nagrade/$', 'object_list', awards_list),

    (r'^umetniki/(?P<object_id>\d+)/$', 'object_detail', artists_detail),
    (r'^festivali/(?P<object_id>\d+)/$', 'object_detail', fests_detail),
    (r'^nagrade/(?P<object_id>\d+)/$', 'object_detail', awards_detail),
    (r'^producenti/(?P<object_id>\d+)/$', 'object_detail', producers_detail),
    (r'^galerije/(?P<object_id>\d+)/$', 'object_detail', gallerys_detail),
)
