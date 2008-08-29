from datetime import datetime
import copy

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required

from forms import ArticleForm
from models import Article, ChangeSet, Category


def wiki_index(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    return render_to_response('wiki/index.html', {'articles': articles, 'categories': categories,
		'admin': '%s/intranet/admin/wiki/' % settings.BASE_URL}, context_instance=RequestContext(request))
wiki_index = login_required(wiki_index)

def article_history(request, id):
    # TODO: use get_object_or_404
    article = Article.objects.get(pk=id)
    changes = article.changeset_set.all()
    return render_to_response('wiki/history.html', {'article': article,
				'changes': changes}, context_instance=RequestContext(request))
article_history = login_required(article_history)

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
view_article = login_required(view_article)

def new_article(request, cat):
    category = Category.objects.get(pk=cat)

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
            return HttpResponseRedirect('../../article/%s/' % new_article.id)
    else:
        form = ArticleForm()

    return render_to_response('wiki/edit.html', {'form': form},
		context_instance=RequestContext(request))
new_article = login_required(new_article)


def edit_article(request, id):
    try:
        article = Article.objects.get(pk=id)
        cat = article.cat
    except Article.DoesNotExist:
        article = None
    old = copy.deepcopy(article)

    if request.method == 'POST':
        

        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            article.cat = cat
            article.save()
            article.create_changeset(old, request.user, form.cleaned_data['comment'])
            return HttpResponseRedirect('../')
    else:
        if article is None:
            form = ArticleForm(initial={'title': title})
        else:
            form = ArticleForm(instance=article)

    return render_to_response('wiki/edit.html', {'form': form},
		context_instance=RequestContext(request))
edit_article = login_required(edit_article)

def view_changeset(request, title, revision):

    # TODO: get obj or 404
    changeset = ChangeSet.objects.get(article__title=title,
                                      revision=int(revision))

    if request.method == "GET":
        return render_to_response('wiki/changeset.html',
                {'article_title': title, 'changeset': changeset},
								context_instance=RequestContext(request))
view_changeset = login_required(view_changeset)

def new_cat(request):
    c = Category(order=1, name=request.POST['cat'])
    print 'before the if'
    if request.POST.has_key('parent'):
        p = Category.objects.get(pk=request.POST['parent'])
        print p
        print 'in the if'
        c.parent= p
        print c.parent
    c.save()
    return HttpResponseRedirect('..')
new_cat = login_required(new_cat)
