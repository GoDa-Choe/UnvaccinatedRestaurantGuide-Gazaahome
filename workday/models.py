from django.db import models
from django.contrib.auth.models import User

from datetime import date, timedelta


class Calculator(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField()
    end_date = models.DateField()

    # ForeignKeys
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} :: {self.author}"


class Leave(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField()
    end_date = models.DateField()

    # ForeignKeys
    calculator = models.ForeignKey(Calculator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_date}~{self.end_date} :: {self.calculator} :: {self.calculator.author}"

    def days(self):
        return self.end_date - self.start_date + timedelta(days=1)
