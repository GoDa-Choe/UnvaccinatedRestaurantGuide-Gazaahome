from django.db import models
from django.contrib.auth.models import User
import cloudinary.models


class Face(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    face = models.ImageField(upload_to='beauty/faces/%Y/%m/%d/')

    GENDER_CHOICES = [
        ("m", "남자"),
        ("f", "여자(업데이트 예정)"),
    ]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="m",

    )

    score = models.FloatField(default=0.0)


    def __str__(self):
        return f"[Face](id-{self.pk})(score-{self.score})(author-{self.author})"
