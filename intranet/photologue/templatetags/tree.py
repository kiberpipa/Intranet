import re

from django import template
from django.conf import settings

from intranet.photologue.models import Gallery

register = template.Library()

url = settings.BASE_URL + '/gallery/'

#def recurse(category):
#    ##prvo link z imenom kategorije
#    result = '<li'
#    if category.parent:
#        result += ' class="closed"'
#    result += '><span class="folder">&nbsp; <a href="%s%d">%s</a></span>\n' % (url, category.id, category.name)
#    #result += '><span class="folder">&nbsp; <a href="%s/new">%s</a>&nbsp;<a href="javascript:;" id="toggle%d">Podkategorija</a></span>\n' % (category.id, category.name, category.id )
#    #result += '<div style="display: none;" id="toggleMe%d"><form method="post" action="cat/"><input type="text" name="cat"><input type="hidden" name="parent" value="%d"><input type="submit" value="Dodaj podkategorijo"></form></div>' % (category.id, category.id)
#
#    galleries = category.gallery.all()
#    children = Category.objects.filter(parent=category)
#
#    if galleries or children:
#        result += '<ul>'
#
#    ##albumi ki spadajo pod to kategorijo
#    if galleries:
#        for i in galleries:
#            result += '	<li><span class="article">&nbsp;<a href="%salbum/%d">%s</a></span></li>\n' % (url, i.id, i.title)
#
#    ##pod kategorije
#    for i in children:
#        if Category.objects.filter(parent=i):
#            if articles:
#                result += recurse(i)
#            else:
#                result += '<ul>\n'
#                result += recurse(i)
#                result += '</ul>\n'
#        else:
#            result += '<li class="closed"><span class="folder">&nbsp; <a href="%s%d">%s</a>&nbsp;</span>\n' % (url, i.id, i.name)    
#            #result += '<div style="display: none;" id="toggleMe%d"><form method="post" action="cat/"><input type="text" name="cat"><input type="hidden" name="parent" value="%d"><input type="submit" value="Dodaj podkategorijo"></form></div>' % (i.id, i.id)
#            galleries2 = i.gallery.all()
#            if galleries2:
#                result += '<ul>'
#                for j in galleries2:
#                    result += '<li><a href="%salbum/%d">%s</a></li>\n' % (url, j.id, j.title)
#                result += '</ul>'
#            result += '</li>\n'
#    
#    if galleries or children:
#        result += '</ul>\n'
#
#    result += '		</li>\n'
#
#    return result
#
#def tree():
#    result = '<ul id="browser" class="filetree">'
#    for category in Category.objects.filter(parent__isnull=True):
#        result += recurse(category)
#
#    result += '</ul>'
#    return result


#register.simple_tag(tree)

