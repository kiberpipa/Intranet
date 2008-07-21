from intranet.org.models import Sodelovanje
from django.contrib import admin

class SodelovanjeAdmin(admin.ModelAdmin):
    search_fields = ('person__name',)
    list_filter = ('tip',)

admin.site.register(Sodelovanje, SodelovanjeAdmin)
