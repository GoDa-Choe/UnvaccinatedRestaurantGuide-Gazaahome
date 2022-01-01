from video_forum.models import VideoComment, Video
from django import forms


class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ('content', 'is_anonymous')
        labels = {
            'content': "",
            'is_anonymous': '익명',
        }
        widgets = {
            'content': forms.Textarea(attrs={'style': "max-height:70px;"}),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'url', 'content', 'category', 'is_anonymous')
        labels = {
            'title': '제목',
            'url': "유튜브 동영상 주소(URL)",
            'content': "내용",
            'category': "카테고리",
            'is_anonymous': "익명",
        }
        widgets = {
            'content': forms.Textarea(attrs={'style': "max-height:100px;"}),
        }
