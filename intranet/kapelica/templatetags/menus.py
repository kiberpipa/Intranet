from django.template import Context, Library, RequestContext
from django import template

register = Library()

from django.views.generic.list_detail import object_list

class MenuArchiveNode(template.Node):
    def __init__(self, object):
        self.object = object

    def render(self, context):
#        c = Context({'form':form,})
        return template.loader.get_template('kapelica/menu_archive.html' % self.object._meta.object_name.lower()).render(context)

def menu_archive(parser, token):
    tag_name, menu_name = token.split_contents()
    m = __import__("intranet.org.models", '','', box_name)
    object = getattr(m, menu_name)
    return MenuArchiveNode(object)
register.tag('menu_archive', menu_archive)
