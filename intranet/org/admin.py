from intranet.org.models import *
from django.contrib import admin

class SodelovanjeAdmin(admin.ModelAdmin):
    search_fields = ('person__name',)
    list_filter = ('tip',)

class DiaryAdmin(admin.ModelAdmin):
    search_fields = ['log_formal','person','task']
    date_hierarchy = 'date'
    list_filter = ['date', 'task', 'author']
    list_display = ('date', 'author', 'task', 'length')

    class Media:
        js = (
              'js/tags.js',
              )
class PersonAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    list_filter = ['project', 'start_date']
    list_display = ['title', 'start_date', 'length']

    class Media:
        js = (
            'js/tags.js',
            )

class StickyNoteAdmin(admin.ModelAdmin):
    search_fields = ['note']
    date_hierarchy = 'due_date'
    list_filter = ['due_date', 'author']

    class Media:
        js = (
            'js/tags.js',
            )

class LendAdmin(admin.ModelAdmin):
    search_fields = ['to_who', 'why', 'note']
    list_display = ['what', 'returned', 'from_who', 'to_who', 'from_date', 'due_date', 'why']

class ScratchpadAdmin(admin.ModelAdmin):
    get_latest_by = "id"

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['note','name','responsible']
    list_display = ['name', 'responsible', 'parent', 'note']
    js = (
            'js/tags.js',
            )

admin.site.register(Category)
admin.site.register(TipSodelovanja)
admin.site.register(Place)
admin.site.register(Email)
admin.site.register(Phone)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Shopping)
admin.site.register(KB)
admin.site.register(KbCategory)
admin.site.register(IntranetImage)


admin.site.register(Sodelovanje, SodelovanjeAdmin)
admin.site.register(Diary, DiaryAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Lend, LendAdmin)
admin.site.register(StickyNote, StickyNoteAdmin)
admin.site.register(Scratchpad, ScratchpadAdmin)
admin.site.register(Project, ProjectAdmin)
