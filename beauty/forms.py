from beauty.models import Face
from django import forms


class FaceForm(forms.ModelForm):

    class Meta:
        model = Face
        fields = ('face', 'gender')
        labels = {
            'face': "사진",
            'gender': "성별",
        }
