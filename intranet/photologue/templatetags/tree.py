import re

from django import template

from intranet.photologue.models import Category, Gallery

register = template.Library()

def recurse(category):
    ##prvo link z imenom kategorije
    result = '<li'
    if category.parent:
        result += ' class="closed"'
    result += '>'
    #result += '><span class="folder">&nbsp; <a href="%s/new">%s</a>&nbsp;<a href="javascript:;" id="toggle%d">Podkategorija</a></span>\n' % (category.id, category.name, category.id )
    #result += '<div style="display: none;" id="toggleMe%d"><form method="post" action="cat/"><input type="text" name="cat"><input type="hidden" name="parent" value="%d"><input type="submit" value="Dodaj podkategorijo"></form></div>' % (category.id, category.id)

    galleries = category.gallery.all()
    children = Category.objects.filter(parent=category)

    if galleries or children:
        result += '<ul>'

    ##clanki ki spadajo pod to kategorijo
    if galleries:
        for i in galleries:
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
            result += '<li class="closed"><span class="folder">&nbsp; <a href="%s/new">%s</a>&nbsp;</span>\n' % (i.id, i.name, i.id)    
            #result += '<div style="display: none;" id="toggleMe%d"><form method="post" action="cat/"><input type="text" name="cat"><input type="hidden" name="parent" value="%d"><input type="submit" value="Dodaj podkategorijo"></form></div>' % (i.id, i.id)
            galleries2 = i.gallery.all()
            if articles2:
                result += '<ul>'
                for j in galleries2:
                    result += '<li><a href="article/%s">%s</a></li>\n' % (j.id, j.title)
                result += '</ul>'
            result += '</li>\n'
    
    if galleries or children:
        result += '</ul>\n'

    result += '		</li>\n'

    return result

def tree():
    result = '<ul id="browser" class="filetree">'
    for category in Category.objects.filter(parent__isnull=True):
        result += recurse(category)

    result += '</ul>'
    return result


register.simple_tag(tree)

