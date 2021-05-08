from django.contrib import admin
from forum.models import Post, Category


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
