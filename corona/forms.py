from django import forms

from corona.models import Restaurant, RestaurantComment
from corona.models import Post, PostComment


class RestaurantCommentForm(forms.ModelForm):
    class Meta:
        model = RestaurantComment
        fields = ('content', 'is_anonymous')
        labels = {
            'content': "",
            'is_anonymous': '익명',
        }

        widgets = {
            'content': forms.Textarea(attrs={'style': "max-height:70px;"}),
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'category', 'unvaccinated_pass',)
        labels = {
            'name': '가게 상호',
            'address': '주소',
            'category': '업종',
            'unvaccinated_pass': '미접종자 거부 여부',
        }


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('content', 'is_anonymous')
        labels = {
            'content': "",
            'is_anonymous': '익명',
        }

        widgets = {
            'content': forms.Textarea(attrs={'style': "max-height:70px;"}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'head_image', 'category', 'is_anonymous')
        labels = {
            'title': '제목',
            'content': "내용",
            'head_image': "사진",
            'category': "카테고리",
            'is_anonymous': '익명',
        }
