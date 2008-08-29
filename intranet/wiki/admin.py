from django.contrib import admin
from models import *

class CategoryAdmin(admin.ModelAdmin):
    ordering = ('order',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article)
admin.site.register(ChangeSet)
