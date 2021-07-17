from django.db import models
from django.contrib.auth.models import User

from workday.models import Calculator

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT


class Barracks(models.Model, HitCountMixin):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    members = models.ManyToManyField(Calculator, blank=True)
    host = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f"{self.pk} :: {self.name}"

    def get_absolute_url(self):
        return f"/barracks/{self.pk}/"

    def num_comments(self):
        return self.guestbook_set.count()


class GuestBook(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    calculator = models.ForeignKey(Calculator, null=True, on_delete=models.SET_NULL)
    barracks = models.ForeignKey(Barracks, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}::{self.calculator.name}::{self.content}"

    def get_absolute_url(self):
        return f"{self.barracks.get_absolute_url()}#guest_book-{self.pk}"


class Invitation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    inviter = models.ForeignKey(Barracks, on_delete=models.CASCADE)
    invitee = models.ForeignKey(Calculator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk} :: {self.inviter}->{self.invitee}"
