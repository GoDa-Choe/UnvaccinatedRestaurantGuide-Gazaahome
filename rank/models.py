from django.db import models
from workday.models import Calculator


class RankingChart(models.Model):
    # ForeignKeys
    calculator = models.OneToOneField(Calculator, on_delete=models.CASCADE, primary_key=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_workday = models.DateField(null=True, blank=True)

    num_workdays = models.IntegerField(null=True, blank=True)
    num_remaindays = models.IntegerField(null=True, blank=True)
    percent = models.FloatField(null=True, blank=True)
    workday_percent = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
