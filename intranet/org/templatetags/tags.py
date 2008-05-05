from django.template import Library
from django import template
from intranet.org.models import Tag

register = Library()

# use for tag cloud
def show_tag_list(parser, token):
    """ {% get_tag_list %}"""
    return TagListObject()

class TagListObject(template.Node):
    def render(self, context):
        context['blog_tags'] = Tag.objects.all()
        return ''

register.tag('get_tag_list', show_tag_list)

