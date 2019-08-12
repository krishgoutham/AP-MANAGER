from django.contrib import admin
from usrhome.models import Event
from .models import Notice, Rent

# Register your models here.
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('head',)

class RentAdmin(admin.ModelAdmin):
        list_display = ('head','order_id','paid')

admin.site.register(Event)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Rent, RentAdmin)