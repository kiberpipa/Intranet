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
