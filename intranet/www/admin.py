from intranet.www.models import *
from django.template.defaultfilters import slugify
from django.contrib import admin
from reversion.admin import VersionAdmin

class NewsAdmin(VersionAdmin):
    fields = ['title', 'image', 'text', 'language']

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        obj.author = request.user
        obj.save()

admin.site.register(Ticker)

admin.site.register(News, NewsAdmin)
