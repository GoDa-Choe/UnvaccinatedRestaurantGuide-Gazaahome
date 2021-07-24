from django.db import models

# Create your models here.
from django.db import models


class Corona(models.Model):
    state_date = models.DateField()
    decided_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
