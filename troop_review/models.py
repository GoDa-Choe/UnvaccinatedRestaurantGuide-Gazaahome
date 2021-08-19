from django.db import models
from django.contrib.auth.models import User

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.contrib.contenttypes.fields import GenericRelation


class Troop(models.Model, HitCountMixin):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.name

    def get_avg_star_rating(self):
        reviews = self.review_set
        star_ratings = [review.star_rating for review in reviews.iterator()]
        return sum(star_ratings) / reviews.count()

    def get_num_reivews(self):
        return self.review_set.count()


class Review(models.Model):
    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    YEAR_CHOICES = [(2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)]
    MONTH_CHOICES = [
        (1, 1), (2, 2), (3, 3),
        (4, 4), (5, 5), (6, 6),
        (7, 7), (8, 8), (9, 9),
        (10, 10), (11, 11), (12, 12),
    ]

    year = models.IntegerField(choices=YEAR_CHOICES)
    month = models.IntegerField(choices=MONTH_CHOICES)

    star_rating = models.IntegerField(choices=RATING_CHOICES)

    duty_assignment = models.CharField(max_length=20)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    troop = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL)
    reviewer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # likes
    likes = models.ManyToManyField(User, blank=True, related_name='liker')

    def num_likes(self):
        return self.likes.count()
