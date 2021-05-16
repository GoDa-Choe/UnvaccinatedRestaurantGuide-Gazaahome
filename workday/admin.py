from django.contrib import admin
from workday.models import Calculator, Leave, Dayoff

admin.site.register(Calculator)
admin.site.register(Leave)
admin.site.register(Dayoff)
