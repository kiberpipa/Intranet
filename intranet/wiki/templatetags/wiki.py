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

def recurse(category, counter=1):
    ##prvo link z imenom kategorije
    result = '		<li><span class="folder">&nbsp; <a href="%s/new">%s</a></span>\n' % (category.id, category.name )

    articles = Article.objects.filter( cat = category)
    ##clanki ki spadajo pod to kategorijo
    if articles:
      result += '			' * counter
      result += '<ul>\n'
      for i in articles:
        result += '			' * counter 
        result += '	<li><span class="article">&nbsp;<a href="article/%s">%s</a></span></li>\n' % (i.id, i.title)
      result += '			' * counter
      result += '</ul>\n'
#      result += '			</ul>\n'


    children = Category.objects.order_by('order').filter(parent=category)
    ##pod kategorije
    for i in children:
        if Category.objects.filter(parent=i):
            result += '			' * counter
            result += '<ul>\n'
            result += recurse(i, counter+1)
            result += '			' * counter
            result += '</ul>\n'
        else:
            result += '<ul><span class="folder">&nbsp; <a href="%s/new">%s</a></span>\n' % (i.id, i.name)    
            for j in Article.objects.filter( cat = i):
                result += '<li><a href="article/%s">%s</a></li>\n' % (j.id, j.title)
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
