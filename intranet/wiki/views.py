from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings

from forms import ArticleForm
from models import Article, ChangeSet, Category


def wiki_index(request):
    articles = Article.objects.all()
    return render_to_response('wiki/index.html', {'articles': articles,
		'admin': '%s/intranet/admin/wiki/' % settings.BASE_URL}, context_instance=RequestContext(request))

def article_history(request, id):
    # TODO: use get_object_or_404
    article = Article.objects.get(pk=id)
    changes = article.changeset_set.all()
    return render_to_response('wiki/history.html', {'article': article,
				'changes': changes}, context_instance=RequestContext(request))
##najdi celo hiearhijo kateri pripada nas article
def parents(article):
    c = article.cat
    parents = []
    while c:
        #parents.insert(0, c.name)
        parents.insert(0, c)
        c = c.parent

    return parents



def view_article(request, id):
    try:
        article = Article.objects.get(pk = id)
    except Article.DoesNotExist:
        article = Article(id=id)

    return render_to_response('wiki/view.html', {'article': article, 'parents': parents(article) }, context_instance=RequestContext(request))

def new_article(request, cat):
    category = Category.objects.filter(pk=cat)[0]

    if request.method == 'POST':

        article = Article()
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            new_article = form.save()
            new_article.cat = category
            new_article.save()
            editor = request.user.get_profile()
            comment = form.cleaned_data.get('comment', '')
            new_article.create_changeset(article, editor, comment)
            return HttpResponseRedirect('../article/%s/' % new_article.id)
    else:
        form = ArticleForm()

    return render_to_response('wiki/edit.html', {'form': form},
		context_instance=RequestContext(request))


def edit_article(request, id):
    try:
        article = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        article = None

    if request.method == 'POST':

        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            new_article = form.save()
            editor = request.user.get_profile()
            comment = form.cleaned_data.get('comment', '')
            new_article.create_changeset(article, editor, comment)
            #return HttpResponseRedirect('../../%s/' % new_article.id)
            return HttpResponseRedirect('../')
    else:
        if article is None:
            form = ArticleForm(initial={'title': title})
        else:
            form = ArticleForm(instance=article)

    return render_to_response('wiki/edit.html', {'form': form},
		context_instance=RequestContext(request))

def view_changeset(request, title, revision):

    # TODO: get obj or 404
    changeset = ChangeSet.objects.get(article__title=title,
                                      revision=int(revision))

    if request.method == "GET":
        return render_to_response('wiki/changeset.html',
                {'article_title': title, 'changeset': changeset},
								context_instance=RequestContext(request))
