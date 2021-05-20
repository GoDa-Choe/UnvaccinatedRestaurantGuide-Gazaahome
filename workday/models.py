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
