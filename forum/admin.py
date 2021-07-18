from django.contrib import admin
from forum.models import Post, Category, Tag, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'content', 'created_at']
    list_display_links = ['id', 'author', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug', ]
    list_display_links = ['id', 'name', ]
    inlines = [
        PostInline,
    ]


class PostshipInline(admin.TabularInline):
    model = Post.tags.through
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'created_at']
    list_display_links = ['id', 'title', ]
    inlines = [
        CommentInline,
        PostshipInline,
    ]
    exclude = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        PostshipInline,
    ]
