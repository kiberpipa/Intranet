from django.template.defaultfilters import slugify
from django.contrib import admin
from reversion.admin import VersionAdmin
from django_mailman.models import List

from intranet.www.models import *
from intranet.www.forms import NewsForm

class NewsAdmin(VersionAdmin):
    form = NewsForm

    date_hierarchy = 'date'
    list_display = ('title', 'date')
    list_filter = ('author', 'language')
    search_fields = ('title', 'text')

    def get_form(self, request, obj=None, **kwargs):
        # pre-populate author field with the current user
        # there is probably a cleaner way to do this - if you know it, pls fix
        form = super(NewsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        if not hasattr(obj, 'author'):
            obj.author = request.user
        obj.save()


admin.site.register(News, NewsAdmin)
admin.site.register(List)
