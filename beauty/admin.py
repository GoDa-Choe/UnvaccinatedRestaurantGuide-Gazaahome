from django.contrib import admin
from beauty.models import Recode


# Register your models here.
@admin.register(Recode)
class CoronaAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created_at']
    list_display_links = ['id', 'author', 'created_at']
