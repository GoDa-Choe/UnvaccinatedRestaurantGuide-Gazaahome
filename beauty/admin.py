from django.contrib import admin
from beauty.models import Face


# Register your models here.
@admin.register(Face)
class FaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'score', 'created_at']
    list_display_links = ['id', 'score', ]
