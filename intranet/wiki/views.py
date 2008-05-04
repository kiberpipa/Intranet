from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response

from forms import ArticleForm
from models import Article, ChangeSet


def wiki_index(request):
    articles = Article.objects.all()
    return render_to_response('wiki/index.html', {'articles': articles})

def article_history(request, title):
    # TODO: use get_object_or_404
    article = Article.objects.get(title=title)
    changes = article.changeset_set.all()
    return render_to_response('wiki/history.html', {'article': article,
                                                    'changes': changes})

def view_article(request, title):
    try:
        article = Article.objects.get(title=title)
    except Article.DoesNotExist:
        article = Article(title=title)
    return render_to_response('wiki/view.html', {'article': article})

def edit_article(request, title):
    try:
        article = Article.objects.get(title=title)
    except Article.DoesNotExist:
        article = None

    if request.method == 'POST':

        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            new_article = form.save()
            editor = request.user.get_profile()
            comment = form.cleaned_data.get('comment', '')
            new_article.create_changeset(article, editor, comment)
            return HttpResponseRedirect('../../%s/' % new_article.title)
    else:
        if article is None:
            form = ArticleForm(initial={'title': title})
        else:
            form = ArticleForm(instance=article)

    return render_to_response('wiki/edit.html', {'form': form})

def view_changeset(request, title, revision):

    # TODO: get obj or 404
    changeset = ChangeSet.objects.get(article__title=title,
                                      revision=int(revision))

    if request.method == "GET":
        return render_to_response('wiki/changeset.html',
                                  {'article_title': title,
                                   'changeset': changeset})
