import re

from django import template

import markdown

WIKI_WORD = r'(?:[A-Z]+[a-z]+){2,}'

wikiwordfier = re.compile(r'\b(%s)\b' % WIKI_WORD)

register = template.Library()

@register.filter
def wikiwordfy(s):
    return wikiwordfier.sub(r'<a href="../\1/">\1</a>', s)


@register.filter
def wikify(s):
    return markdown.markdown(s)

#import StringIO
#
#from mwlib import uparser, htmlwriter, dummydb
#def mwlib(value):
#    out = StringIO.StringIO()
#    p = uparser.parseString('test', raw=value, wikidb=dummydb.DummyDB())
#    print list(p.allchildren())
#    w = htmlwriter.HTMLWriter(out)
#    w.write(p)
#    return out.getvalue()
#
#
from mw import parse
register.filter('mw', parse)


