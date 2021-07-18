from workday.models import Calculator, Leave, Dayoff
from django.contrib import admin
from barracks.admin import MembershipInline


class LeaveInline(admin.TabularInline):
    model = Leave
    extra = 0


class DayoffInline(admin.TabularInline):
    model = Dayoff
    extra = 0


@admin.register(Calculator)
class CalculatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'start_date', 'end_date', 'author']
    list_display_links = ['id', 'name']
    inlines = [
        LeaveInline,
        MembershipInline,
    ]


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'calculator', 'type', 'start_date', 'end_date', 'created_at']
    list_display_links = ['id', 'calculator']


@admin.register(Dayoff)
class DayoffAdmin(admin.ModelAdmin):
    list_display = ['id', 'calculator', 'date', 'created_at']
    list_display_links = ['id', 'calculator']
