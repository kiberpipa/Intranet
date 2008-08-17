from django.conf.urls.defaults import *

from intranet.wiki.templatetags.wiki import WIKI_WORD
from wiki import views

article_re = r'^article/(?P<id>%s)' % WIKI_WORD

urlpatterns = patterns('',
    url(r'^$', views.wiki_index,
        name='wiki_index'),

    url(article_re + r'/$', views.view_article,
        name='wiki_article'),

    url('^(?P<cat>[0-9]+)/new/$', views.new_article),

    url(article_re + r'/edit/$', views.edit_article,
        name='wiki_edit_article'),

    url(article_re + r'/history/$', views.article_history,
        name='wiki_article_history'),

    url(r'/'.join([r'(?P<title>[A-Za-z]+)', r'changeset', '(?P<revision>\d+)', r'$']),
        views.view_changeset, name='wiki_changeset')

)
