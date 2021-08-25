# Create your models here.
from django.db import models


class Corona(models.Model):
    state_date = models.DateField()
    decided_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Statistics(models.Model):
    state_date = models.DateField(verbose_name="date")

    user_count = models.IntegerField(verbose_name="user")

    calculator_count = models.IntegerField(verbose_name="calculator")
    leave_count = models.IntegerField(verbose_name="leave")

    barracks_count = models.IntegerField(verbose_name="barracks")
    guest_book_count = models.IntegerField(verbose_name="guest book")

    troop_count = models.IntegerField(verbose_name="troop")
    review_count = models.IntegerField(verbose_name="review")

    post_count = models.IntegerField(verbose_name="post")
    comment_count = models.IntegerField(verbose_name="comment")

    user_increment = models.IntegerField(verbose_name="user increment")
    calculator_increment = models.IntegerField(verbose_name="calculator increment")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
