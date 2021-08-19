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
        fields = ('year', 'month', 'duty_assignment', 'star_rating', 'content')
        labels = {
            'year': '입대 연도',
            'month': '입대 월',
            'duty_assignment': '보직',
            'star_rating': '별점',
            'content': '내용',
        }
