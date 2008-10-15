import re

from django import template

from intranet.wiki.models import Category, Article

#WIKI_WORD = r'(?:[A-Z]+[a-z]+){2,}'
WIKI_WORD = r'(?:[^/]*)'

wikiwordfier = re.compile(r'\b(%s)\b' % WIKI_WORD)

register = template.Library()

@register.filter
def wikiwordfy(s):
    return wikiwordfier.sub(r'<a href="../\1/">\1</a>', s)


#not used and unncessary dependency at this point
#import markdown
#@register.filter
#def wikify(s):
#    return markdown.markdown(s)

##mw wiki syntax parser
from mw import parse
register.filter('mw', parse)
