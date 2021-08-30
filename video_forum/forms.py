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
        fields = ('title', 'url', 'is_anonymous')
        labels = {
            'title': '제목',
            'url': "유튜브 동영상 주소(url)",
            'is_anonymous': "익명",
        }
