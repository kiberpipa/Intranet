from django.template.defaultfilters import slugify
from django.contrib import admin
from reversion.admin import VersionAdmin
from django_mailman.models import List

from intranet.www.models import *


class NewsAdmin(VersionAdmin):
    fields = ['title', 'image', 'text', 'language', 'author']
    date_hierarchy = 'date'
    list_display = ('title', 'date')
    list_filter = ('author', 'language')
    search_fields = ('title', 'text')

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        if not obj.author:
            obj.author = request.user
        obj.save()


admin.site.register(News, NewsAdmin)
admin.site.register(List)
