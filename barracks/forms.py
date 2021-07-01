from barracks.models import Barracks, Invitation
from django.forms import ModelForm, ValidationError, Form, TextInput
from django.forms import CharField


class BarracksForm(ModelForm):
    class Meta:
        model = Barracks
        fields = ('name',)
        labels = {
            'name': '생활관 이름',
        }
