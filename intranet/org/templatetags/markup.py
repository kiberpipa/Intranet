from django.template import Context, Library, RequestContext
from django.template import resolve_variable

register = Library()

def textile(value):
    try:
        import textile
    except ImportError:
        return value
    else:
        return textile.textile(value, encoding='utf-8')


register.filter(textile)
