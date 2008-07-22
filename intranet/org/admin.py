#from intranet.org.models import Sodelovanje, Person, UserProfile
from intranet.org.models import *
from django.contrib import admin

class SodelovanjeAdmin(admin.ModelAdmin):
    search_fields = ('person__name',)
    list_filter = ('tip',)

admin.site.register(Sodelovanje, SodelovanjeAdmin)
admin.site.register(Person)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(TipSodelovanja)
admin.site.register(Project)
admin.site.register(Place)
