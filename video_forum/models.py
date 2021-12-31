from django.db import models
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.contrib.contenttypes.fields import GenericRelation


class VideoTag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class VideoCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def get_num_videos(self):
        return self.video_set.count()


class Video(models.Model, HitCountMixin):
    title = models.CharField(max_length=40)
    url = EmbedVideoField()
    content = models.TextField(null=True, blank=True)
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    # likes
    likes = models.ManyToManyField(User, blank=True, related_name="video_likers")

    # ForeignKeys
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(VideoTag, blank=True)
    category = models.ForeignKey(VideoCategory, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"[비디오]::{self.pk}::{self.author}::{self.title[:20]}"

    def get_absolute_url(self):
        return f"/corona/video_forum/{self.pk}/"

    def num_likes(self):
        return self.likes.count()

    def num_comments(self):
        return self.videocomment_set.count()


class VideoComment(models.Model):
    content = models.TextField()
    is_anonymous = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # likes
    likes = models.ManyToManyField(User, blank=True, related_name="video_comment_likers")

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}::{self.video.title}"

    def get_absolute_url(self):
        return f"{self.video.get_absolute_url()}#comment-{self.pk}"

    def num_likes(self):
        return self.likes.count()
