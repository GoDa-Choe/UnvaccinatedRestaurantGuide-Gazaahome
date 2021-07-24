from django.db import models


class Corona(models.Model):
    state_date = models.DateField()
    decideCnt = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
