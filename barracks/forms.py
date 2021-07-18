from django.forms import ModelForm, ValidationError, Form, TextInput
from django.forms import CharField

from barracks.models import Barracks, Invitation, GuestBook
from workday.models import Calculator


class BarracksForm(ModelForm):
    class Meta:
        model = Barracks
        fields = ('name',)
        labels = {
            'name': '생활관 이름',
        }


class GuestBookForm(ModelForm):
    class Meta:
        model = GuestBook
        fields = ('content',)
        labels = {
            'content': ""
        }


SEARCH_ATTRS = {
    "placeholder": "친구 계산기 검색으로 초대",
}


class CalculatorSearchForm(Form):
    calculator_name = CharField(max_length=30, label="", widget=TextInput(attrs=SEARCH_ATTRS))

    def clean_calculator_name(self):
        calculator_name = self.cleaned_data.get('calculator_name')
        calculator = Calculator.objects.filter(name__icontains=calculator_name).first()
        if calculator:
            return calculator_name
        else:
            raise ValidationError(f"존재하지 않습니다")
