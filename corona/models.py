from django.db import models
from django.contrib.auth.models import User

from markdownx.models import MarkdownxField
from markdownx.utils import markdown

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.contrib.contenttypes.fields import GenericRelation

from django.utils.safestring import mark_safe


class UnvaccinatedPass(models.Model):
    type = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.type


class RestaurantTag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    # slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'RestaurantCategories'


ADDRESS_HELP_TEXT = """
    <a href="https://map.naver.com/v5/" class="text-decoration-none small" target="_blank">
        <img src="https://res.cloudinary.com/hyzq6bxmk/image/upload/v1640650504/static/corona/naver_map_yc6xld.png" 
        style="width: 20px; height: 20px">
        네이버 지도에서 알아보기
    </a>
"""

SAFE_ADDRESS_HELP_TEXT = mark_safe(ADDRESS_HELP_TEXT.strip())


class Restaurant(models.Model, HitCountMixin):
    name = models.CharField(max_length=40, unique=True)

    address = models.CharField(max_length=200, blank=False, null=True,
                               help_text=SAFE_ADDRESS_HELP_TEXT)

    region = models.CharField(max_length=10, blank=True, null=True, default="")

    content = models.TextField(null=True, blank=True, default="")

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    verifieded = models.BooleanField(default=False)

    url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(RestaurantCategory, null=True, on_delete=models.SET_NULL,
                                 help_text="PCR 음성 필요 여부는 <태그>를 통해 작성해주시면 감사하겠습니다.")
    tags = models.ManyToManyField(RestaurantTag, blank=True, )
    unvaccinated_pass = models.ForeignKey(UnvaccinatedPass, null=True, on_delete=models.SET_NULL,
                                          help_text="이용가능 여부가 궁금하시면 <궁금>으로 설정해주세요")

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
    image = models.ImageField(null=True, upload_to='corona/restaurant/comments/%Y/%m/%d/', blank=True, default=None)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    # image2 = models.ImageField(upload_to='corona/restaurant/comments/%Y/%m/%d/', null=True, blank=True)
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


class RestaurantDeleteRequest(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}::{self.restaurant.name}::{self.content}"


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


class FastRestaurant(models.Model):
    name = models.CharField(max_length=40, unique=True)

    address = models.CharField(max_length=200, blank=False, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    verifieded = models.BooleanField(default=False)

    url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.CharField(max_length=20)
    tags = models.CharField(max_length=50, blank=True)
    unvaccinated_pass = models.CharField(max_length=20)

    # likes and dislikes and comments
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    num_hits = models.IntegerField(default=1)

    base = models.ForeignKey(Restaurant, default=1, on_delete=models.CASCADE)
