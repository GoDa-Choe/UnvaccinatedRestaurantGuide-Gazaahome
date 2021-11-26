from django.db import models
from django.contrib.auth.models import User

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.contrib.contenttypes.fields import GenericRelation
import math


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
        avr_star_rating = sum(star_ratings) / reviews.count() if reviews.count() else 0
        return round(avr_star_rating, 2)

    def get_full_star(self):
        start = self.get_avg_star_rating()
        integer = math.trunc(start)
        floating = start - integer

        full_star = integer

        if floating > 0.75:
            full_star += 1

        return full_star

    def get_half_star(self):
        start = self.get_avg_star_rating()
        integer = math.trunc(start)
        floating = start - integer

        half_star = 0

        if floating > 0.25:
            half_star += 1

        return half_star

    def get_empty_star(self):

        full_star = self.get_full_star()
        half_star = self.get_half_star()

        empty_star = 5 - (full_star + half_star)
        return empty_star

    def get_num_reivews(self):
        return self.review_set.count()


class Review(models.Model):
    YEAR_CHOICES = [(2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)]
    MONTH_CHOICES = [
        (1, 1), (2, 2), (3, 3),
        (4, 4), (5, 5), (6, 6),
        (7, 7), (8, 8), (9, 9),
        (10, 10), (11, 11), (12, 12),
    ]

    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    TRANING_CHOICES = (
        ('very_high', '매우 많음'),
        ('high', '많음'),
        ('nomal', '보통'),
        ('low', '적음'),
        ('very_low', '매우 적음'),
    )
    DISCIPLINE_CHOICES = (
        ('very_high', '매우 빡셈'),
        ('high', '빡셈'),
        ('nomal', '보통'),
        ('low', '빠짐'),
        ('very_low', '매우 빠짐'),
    )
    LEAVE_CHOICES = (
        ('very_high', '매우 많음'),
        ('high', '많음'),
        ('nomal', '보통'),
        ('low', '적음'),
        ('very_low', '매우 적음'),
    )

    year = models.IntegerField(choices=YEAR_CHOICES)
    month = models.IntegerField(choices=MONTH_CHOICES)
    duty_assignment = models.CharField(max_length=20)

    star_rating = models.IntegerField(choices=RATING_CHOICES)

    training = models.CharField(max_length=9, choices=TRANING_CHOICES, default='nomal')
    discipline = models.CharField(max_length=9, choices=DISCIPLINE_CHOICES, default='nomal')
    leave = models.CharField(max_length=9, choices=LEAVE_CHOICES, default='nomal')

    content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    troop = models.ForeignKey(Troop, null=True, on_delete=models.SET_NULL)
    reviewer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # likes
    likes = models.ManyToManyField(User, blank=True, related_name='liker')

    def num_likes(self):
        return self.likes.count()
