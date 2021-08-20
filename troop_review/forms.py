from troop_review.models import Troop, Review
from django.forms import ModelForm


# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('content',)
#         labels = {
#             'content':""
#         }


class TroopForm(ModelForm):
    class Meta:
        model = Troop
        fields = ('name',)
        labels = {
            'name': '부대명',
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('year', 'month', 'duty_assignment', 'star_rating', 'training', 'discipline','leave', 'content')

        labels = {
            'year': '기준 군번(연도)',
            'month': '기준 군번(월)',
            'duty_assignment': '보직',
            'star_rating': '별점',
            'training': '훈련(업무)량',
            'discipline': '군기',
            'leave': '휴가량',
            'content': '내용',
        }
