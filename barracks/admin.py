from django.contrib import admin
from barracks.models import Barracks, Invitation, GuestBook
from django.contrib import admin


@admin.register(Barracks)
class BarracksAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'host']
    list_display_links = ['id', 'name']


admin.site.register(Invitation)
admin.site.register(GuestBook)
