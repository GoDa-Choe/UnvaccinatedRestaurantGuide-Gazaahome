from django.contrib import admin
from home.models import Corona


@admin.register(Corona)
class CoronaAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_date', 'decided_count', 'created_at', ]
    list_display_links = ['id', 'state_date', ]
