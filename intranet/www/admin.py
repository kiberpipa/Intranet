from intranet.www.models import *
from django.template.defaultfilters import slugify
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'image', 'text']

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        obj.author = request.user
        obj.save()

admin.site.register(Ticker)
admin.site.register(Video)

admin.site.register(News, NewsAdmin)
