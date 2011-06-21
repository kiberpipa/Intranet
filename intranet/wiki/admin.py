from django.contrib import admin

from models import *

from reversion.admin import VersionAdmin

class CategoryAdmin(VersionAdmin):
    ordering = ('order',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(ChangeSet)
