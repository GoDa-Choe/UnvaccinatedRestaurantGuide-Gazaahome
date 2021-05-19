from forum.models import Comment, Post
from django.forms import ModelForm


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content':""
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'head_image', 'category')
        labels = {
            'title': '제목',
            'content': "내용",
            'head_image': "사진",
            'category': "카테고리",
        }
