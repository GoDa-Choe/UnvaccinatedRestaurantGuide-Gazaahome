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

    # hit_counts
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f"{self.pk} :: {self.name}"

    def get_absolute_url(self):
        return f"/barracks/{self.pk}/"


class Invitation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKeys
    inviter = models.ForeignKey(Barracks, on_delete=models.CASCADE)
    invitee = models.ForeignKey(Calculator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk} :: {self.inviter}->{self.invitee}"
