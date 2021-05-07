from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='forum/images/%Y/%m/%d/', blank=True)

    # author 추후 추가예정

    def __str__(self):
        return f"[{self.pk}] {self.title}"

    def get_absolute_url(self):
        return f"/forum/{self.pk}/"
