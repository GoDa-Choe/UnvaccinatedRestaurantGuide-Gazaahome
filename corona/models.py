from django.db import models
from django.contrib.auth.models import User

from markdownx.models import MarkdownxField
from markdownx.utils import markdown

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.contrib.contenttypes.fields import GenericRelation


class UnvaccinatedPass(models.Model):
    type = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.type


class RestaurantTag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'RestaurantCategories'


class Restaurant(models.Model, HitCountMixin):
    name = models.CharField(max_length=40)

    address = models.CharField(max_length=200, blank=True, null=True,
                               help_text="주소 생략시 <가게 상호>을 구체적으로 입력해주세요. (예시: 최고다삽겹살 고다역점)")

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    verifieded = models.BooleanField(default=False)

    url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(RestaurantCategory, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(RestaurantTag, blank=True)
    unvaccinated_pass = models.ForeignKey(UnvaccinatedPass, null=True, on_delete=models.SET_NULL)

    # likes and dislikes
    likes = models.ManyToManyField(User, blank=True, related_name="restaurant_likers")
    dislikes = models.ManyToManyField(User, blank=True, related_name="restaurant_dislikers")

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f"[식당]::{self.pk}::{self.name}::{self.unvaccinated_pass}::{self.verifieded}"

    def get_absolute_url(self):
        return f"/corona/unvaccinated_restaurant/{self.pk}/"

    def num_likes(self):
        return self.likes.count()

    def num_dislikes(self):
        return self.dislikes.count()

    def num_comments(self):
        return self.restaurantcomment_set.count()


class RestaurantComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    content = models.TextField()

    is_anonymous = models.BooleanField(default=True)

    likes = models.ManyToManyField(User, blank=True, related_name="restaurant_comment_likers")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}::{self.restaurant.name}::{self.content}"

    def get_absolute_url(self):
        return f"{self.restaurant.get_absolute_url()}#comment-{self.pk}"

    def num_likes(self):
        return self.likes.count()


class PostCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/corona/post/category/{self.name}/"

    class Meta:
        verbose_name_plural = 'PostCategories'


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=40)
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='corona/post/images/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="corona_post_author")
    is_anonymous = models.BooleanField(default=True)
    category = models.ForeignKey(PostCategory, null=True, on_delete=models.SET_NULL)

    # likes and dislikes
    likes = models.ManyToManyField(User, blank=True, related_name="post_likers")
    dislikes = models.ManyToManyField(User, blank=True, related_name="post_dislikers")

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f"[게시글]::{self.pk}::{self.author}::{self.title[:20]}"

    def get_absolute_url(self):
        return f"/corona/post/{self.pk}/"

    def get_content_markdown(self):
        return markdown(self.content)

    def num_likes(self):
        return self.likes.count()

    def num_dislikes(self):
        return self.dislikes.count()

    def num_comments(self):
        return self.postcomment_set.count()


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    content = models.TextField()

    is_anonymous = models.BooleanField(default=True)

    likes = models.ManyToManyField(User, blank=True, related_name="post_comment_likers")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}::{self.post.title}::{self.content}"

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.pk}"

    def num_likes(self):
        return self.likes.count()
