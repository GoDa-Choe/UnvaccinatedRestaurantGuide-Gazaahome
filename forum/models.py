from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='forum/images/%Y/%m/%d/', blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"[{self.pk}] {self.title} :: {self.author}"

    def get_absolute_url(self):
        return f"/forum/{self.pk}/"
