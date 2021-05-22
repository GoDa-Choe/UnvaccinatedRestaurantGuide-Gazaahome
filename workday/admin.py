from django.contrib import admin
from workday.models import Calculator, Leave, Dayoff
from django.contrib import admin


@admin.register(Calculator)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'start_date', 'end_date', 'author']
    list_display_links = ['id', 'name']


admin.site.register(Leave)
admin.site.register(Dayoff)
