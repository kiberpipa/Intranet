
from datetime import datetime
import difflib

from django.db import models
from django.contrib.auth.models import User
from intranet.org.models import UserProfile

###FIXME -- write a proper user profile
#class WikiUser(models.Model):
#    """The wiki user profile.
#    Set AUTH_PROFILE_MODULE = 'wiki.WikiUser'
#    to use this class as the site user profile.
#    """
#    user = models.ForeignKey(User, unique=True)
#
##    class Admin:
##        pass
#
#    def __unicode__(self):
#        return unicode(self.user)

class Category(models.Model):
    order = models.PositiveIntegerField()
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name


    class Admin: 
        pass


    class Meta:
        ordering = ('order',)


class Article(models.Model):
    """A wiki page.
    """
    #title = models.CharField("Article Title", max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField("Article Content")
    cat = models.ForeignKey(Category, blank=True, null=True)

    class Admin:
        pass

    @models.permalink
    def get_absolute_url(self):
        return ('wiki_view_article', (self.title,))

    def create_changeset(self, old, editor, comment):
        '''Create a ChangeSet instance with the old content.'''
        new = self

        try:
            latest = ChangeSet.objects.filter(article=self).latest('modified')
            revision = latest.revision + 1
        except ChangeSet.DoesNotExist:
            revision = 1

        changes_args = {'article': self,
                        'editor': editor,
                        'comment': comment,
                        'revision': revision}
        try:
            changes_args.update({'old_content': old.content,
                                 'old_title': old.title})
        except AttributeError:
            # old is None
            changes_args['old_content'] = ''

        ChangeSet.objects.create(**changes_args)

    def __unicode__(self):
        return self.title

class ChangeSet(models.Model):
    """A report of an older version of an Article."""
    #article = models.ForeignKey(Article, edit_inline=models.TABULAR)
    article = models.ForeignKey(Article)
    #editor = models.ForeignKey(WikiUser)
    editor = models.ForeignKey(User)
    revision = models.IntegerField("Revision Number")
    old_title = models.CharField("Old Title", max_length=50, blank=True)
    #old_title = models.CharField(max_length=50, blank=True)
    old_content = models.TextField("Old Content", blank=True)
    comment = models.CharField("Editor comment", max_length=50, blank=True)
    #comment = models.CharField(max_length=50, blank=True)
    modified = models.DateTimeField("Modified at", default=datetime.now,
                                    core=True)

    class Meta:
        get_latest_by  = 'modified'

    class Admin:
        pass

    @models.permalink
    def get_absolute_url(self):
        return ('wiki_changeset',
                (self.article.title,
                 self.revision))

    def diff(self):
        '''Create a HTML diff table.'''
        try:
            newer_version = self.get_next_by_modified(article=self.article)
            new_content = newer_version.old_content
        except ChangeSet.DoesNotExist:
            # last change.
            new_content = self.article.content
        return difflib.HtmlDiff().make_table(self.old_content.splitlines(),
                                             new_content.splitlines())
