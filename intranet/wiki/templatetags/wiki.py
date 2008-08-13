import re

from django import template

import markdown
from intranet.wiki.models import Category, Article

#WIKI_WORD = r'(?:[A-Z]+[a-z]+){2,}'
WIKI_WORD = r'(?:[^/]*)'

wikiwordfier = re.compile(r'\b(%s)\b' % WIKI_WORD)

register = template.Library()

@register.filter
def wikiwordfy(s):
    return wikiwordfier.sub(r'<a href="../\1/">\1</a>', s)


@register.filter
def wikify(s):
    return markdown.markdown(s)

##mw wiki syntax parser
from mw import parse
register.filter('mw', parse)

def recurse(category):
    ##prvo link z imenom kategorije
    result = '<li'
    if category.parent:
        result += ' class="closed"'
    result += '><span class="folder">&nbsp; <a href="%s/new">%s</a></span>\n' % (category.id, category.name )

    articles = Article.objects.filter( cat = category)
    children = Category.objects.order_by('order').filter(parent=category)

    if articles or children:
        result += '<ul>'

    ##clanki ki spadajo pod to kategorijo
    if articles:
        for i in articles:
            result += '	<li><span class="article">&nbsp;<a href="article/%s">%s</a></span></li>\n' % (i.id, i.title)

    ##pod kategorije
    for i in children:
        if Category.objects.filter(parent=i):
            if articles:
                result += recurse(i)
            else:
                result += '<ul>\n'
                result += recurse(i)
                result += '</ul>\n'
        else:
            result += '<li class="closed"><span class="folder">&nbsp; <a href="%s/new">%s</a></span>\n' % (i.id, i.name)    
            articles2 = Article.objects.filter( cat = i)
            if articles2:
                result += '<ul>'
                for j in Article.objects.filter( cat = i):
                    result += '<li><a href="article/%s">%s</a></li>\n' % (j.id, j.title)
                result += '</ul>'
            result += '</li>\n'
    
    if articles or children:
        result += '</ul>\n'

    result += '		</li>\n'

    return result

def wiki_index():
    result = '<ul id="browser" class="filetree">'
    for category in Category.objects.order_by('order').filter(parent__isnull=True):
        result += recurse(category)

    result += '</ul>'
    return result


register.simple_tag(wiki_index)
