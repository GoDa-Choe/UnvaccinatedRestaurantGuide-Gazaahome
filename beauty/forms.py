from beauty.models import Recode
from django import forms


class TestForm(forms.Form):
    face = forms.ImageField(label="사진")
    GENDER_CHOICES = [
        ("m", "남자"),
        ("f", "여자"),
    ]
    gender = forms.ChoiceField(label='성별', widget=forms.RadioSelect, choices=GENDER_CHOICES)


class RecordForm(forms.ModelForm):
    class Meta:
        model = Recode
        fields = ('face', 'gender',)
        labels = {
            'face': "사진",
            'gender': '성별',
        }
        GENDER_CHOICES = [
            ("m", "남자"),
            ("f", "여자"),
        ]
        widgets = {
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
        }
