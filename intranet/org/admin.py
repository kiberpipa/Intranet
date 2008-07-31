#from intranet.org.models import Sodelovanje, Person, UserProfile
from intranet.org.models import *
from django.contrib import admin

class SodelovanjeAdmin(admin.ModelAdmin):
    search_fields = ('person__name',)
    list_filter = ('tip',)

class BugAdmin(admin.ModelAdmin):
        verbose_name = 'Hrosc'
        verbose_name_plural = 'Hrosci'
        search_fields = ['note','name','assign']
        #list_filter = ['resolved', 'assign']
        list_filter = ['assign']
        #list_display = ['name', 'id', 'resolved', 'author', 'assign']
        #list_display = ['name', 'id', 'author', 'assign']
        list_display = ['name', 'id', 'author']
        #ordering = ['resolved']

admin.site.register(Sodelovanje, SodelovanjeAdmin)
admin.site.register(Person)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(TipSodelovanja)
admin.site.register(TipMedija)
admin.site.register(TipPrispevka)
admin.site.register(Clipping)
admin.site.register(Medij)
admin.site.register(Project)
admin.site.register(Place)
admin.site.register(Bug, BugAdmin)
