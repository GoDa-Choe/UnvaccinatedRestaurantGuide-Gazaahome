from django import forms

from corona.models import Restaurant, RestaurantComment, RestaurantDeleteRequest
from corona.models import Post, PostComment


class RestaurantCommentForm(forms.ModelForm):
    class Meta:
        model = RestaurantComment
        fields = ('content',
                  'image',
                  'is_anonymous')
        labels = {
            'content': "",
            'image': "사진",
            'is_anonymous': '익명',
        }

        widgets = {
            'content': forms.Textarea(attrs={'style': "max-height:90px;"}),
        }


class Restaurant1stForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'category', 'unvaccinated_pass')
        labels = {
            'name': '가게 상호',
            'address': '주소',
            'category': '업종',
            'unvaccinated_pass': '미접종자 거부 여부',
        }


class Restaurant2ndForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = (
            'content',
            'url',
        )
        labels = {
            'content': '내용',
            'url': '네이버 지도 바로가기 주소(URL)',
        }

        widgets = {
            'url': forms.URLInput(attrs={'placeholder': '생략 가능합니다'}),
        }


class RestaurantUpdateForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'category', 'unvaccinated_pass', 'url')
        labels = {
            'name': '가게 상호',
            'address': '주소',
            'category': '업종',
            'unvaccinated_pass': '미접종자 거부 여부',
            'url': '네이버 지도 바로가기 주소(URL)',
        }

        widgets = {
            'url': forms.URLInput(attrs={'placeholder': '생략 가능합니다'}),
        }


class RestaurantUpdateAuthorForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'category', 'unvaccinated_pass',
                  'content',
                  'url')
        labels = {
            'name': '가게 상호',
            'address': '주소',
            'category': '업종',
            'unvaccinated_pass': '미접종자 거부 여부',
            'content': '내용',
            'url': '네이버 지도 바로가기 주소(URL)',
        }

        widgets = {
            'url': forms.URLInput(attrs={'placeholder': '생략 가능합니다'}),
            'content': forms.Textarea(attrs={'style': "max-height:90px;"}),
        }


SEARCH_ATTRS = {
    "placeholder": "식당을 검색해보세요",
}


class RestaurantSearchForm(forms.Form):
    search_string = forms.CharField(max_length=40, label="", widget=forms.TextInput(attrs=SEARCH_ATTRS))
    prefix = "restaurant_search_form"


class FastRestaurantSearchForm(forms.Form):
    search_string = forms.CharField(max_length=40, label="", widget=forms.TextInput(attrs=SEARCH_ATTRS))
    prefix = "restaurant_search_form"


class RestaurantDeleteRequestForm(forms.ModelForm):
    class Meta:
        model = RestaurantDeleteRequest
        fields = ('content',)
        labels = {
            'content': '삭제요청 내용',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '삭제 요청 승인까지 약간의 시간이 소요될 수 있습니다.'}),
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
