from workday.models import Calculator
from django.forms import ModelForm


class CalculatorForm(ModelForm):
    class Meta:
        model = Calculator
        fields = ('name', 'start_date', 'end_date')
        labels = {
            'name': '실출근 계산기 이름',
            'start_date': '입대일',
            'end_date': '전역일',
        }
