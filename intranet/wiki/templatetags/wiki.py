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
    ##some magic html/js thingy
#   html = 'onclick="d=this.parentNode.getElementsByTagName(\'ol\')[0];d.style.display=d.style.display==\'none\'?\'block\':\'none\'; return false"' 

    ##prvo link z imenom kategorije
    result = '		<li><span class="folder">&nbsp; <a href="%s/new">%s</a></span>\n' % (category.id, category.name )

    articles = Article.objects.filter( cat = category)
    ##clanki ki spadajo pod to kategorijo
    if articles:
      result += '			' * counter
      result += '<ul>\n'
      for i in articles:
        result += '			' * counter 
        result += '	<li><span class="article">&nbsp;%s</span></li>\n' % i.title
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
                result += '<li>%s</li>\n' % j.title
            result += '</ul>\n'
    




#    result += '		</ul>'


    result += '		</li>\n'


    #if articles or children:
    return result

def wiki_index():
    #result = '<ol>'
    #return 'tralalal'
    #i=''
    #for i in Category.objects.all():
        #i+=i.name.__str__()
    #return Category.objects.all()
    #return i
    result = '<ul id="browser" class="filetree">'
    for category in Category.objects.order_by('order').filter(parent__isnull=True):
        #print "the i: %s" % category
        result += recurse(category)

    result += '</ul>'
    return result


register.simple_tag(wiki_index)
