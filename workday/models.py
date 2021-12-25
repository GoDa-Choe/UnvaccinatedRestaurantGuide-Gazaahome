from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT

DATE_FORMAT = "날짜형식: 2021-01-01"


class Calculator(models.Model, HitCountMixin):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField(help_text=DATE_FORMAT)
    end_date = models.DateField(help_text=DATE_FORMAT)

    is_open = models.BooleanField(default=True)

    # ForeignKeys
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f"[계산기]::{self.name}::{self.author}"


class Leave(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField(help_text=DATE_FORMAT)
    end_date = models.DateField(help_text=DATE_FORMAT)

    LEAVE_CHOICES = (
        ('ye', '연가'),
        ('po', '포상'),
        ('wi', '위로'),
        ('bo', '보상'),
        ('ch', '청원'),
        ('tp', '예정'),
    )
    type = models.CharField(max_length=2, choices=LEAVE_CHOICES)

    # ForeignKeys
    calculator = models.ForeignKey(Calculator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_date}~{self.end_date} :: {self.calculator} :: {self.calculator.author}"

    def days(self):
        return self.end_date - self.start_date + timedelta(days=1)

    def get_leaves(self):
        leaves = []
        current = self.start_date
        while current <= self.end_date:
            leaves.append(current)
            current += timedelta(days=1)
        return leaves


class Dayoff(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date = models.DateField()

    # ForeignKeys
    calculator = models.ForeignKey(Calculator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} :: {self.calculator.name} :: {self.calculator.author}"
