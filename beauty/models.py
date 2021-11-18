from django.db import models
from django.contrib.auth.models import User


class Recode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    face = models.ImageField(upload_to='beauty/faces/%Y/%m/%d/')

    GENDER_CHOICES = [
        ("m", "남자"),
        ("f", "여자"),
    ]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="m",

    )

    score = models.FloatField()

    # ForeignKeys
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"[Beauty Recode](id-{self.pk})(author-{self.author})"
