from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from video_forum.models import Video, VideoTag, VideoComment


@admin.register(Video)
class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'url', 'is_anonymous', 'created_at']
    list_display_links = ['id', 'author', ]


@admin.register(VideoTag)
class VideoTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name', ]


@admin.register(VideoComment)
class VideoCommentAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ['id', 'author', 'video', 'content', 'is_anonymous', 'created_at']
    list_display_links = ['id', 'author', ]
