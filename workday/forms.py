from workday.models import Calculator, Leave, Dayoff
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


class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ('start_date', 'end_date')
        labels = {
            'start_date': '휴가 시작일',
            'end_date': '휴가 종료일',
        }


class DayoffForm(ModelForm):
    class Meta:
        model = Dayoff
        fields = ('date', 'calculator')
