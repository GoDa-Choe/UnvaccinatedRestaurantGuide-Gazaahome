from corona.models import Restaurant, RestaurantComment
from django import forms


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
            'name': '상호',
            'address': '주소',
            'category': '업종',
            'unvaccinated_pass': '미접종자 거부 여부',
        }
