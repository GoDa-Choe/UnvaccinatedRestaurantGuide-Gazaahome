from django.db import models
from django.contrib.auth.models import User

from markdownx.models import MarkdownxField
from markdownx.utils import markdown

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.contrib.contenttypes.fields import GenericRelation


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    priority = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=40)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='forum/images/%Y/%m/%d/', blank=True)

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    # likes
    likes = models.ManyToManyField(User, blank=True, related_name="likers")

    # ForeignKeys
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"[게시글]::{self.pk}::{self.author}::{self.title[:20]}"

    def get_absolute_url(self):
        return f"/forum/{self.pk}/"

    def get_content_markdown(self):
        return markdown(self.content)

    def num_likes(self):
        return self.likes.count()

    def num_comments(self):
        return self.comment_set.count()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}::{self.post.title}::{self.content}"

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.pk}"
