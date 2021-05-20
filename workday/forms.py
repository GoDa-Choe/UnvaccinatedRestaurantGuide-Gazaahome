from workday.models import Calculator, Leave, Dayoff
from django.forms import ModelForm, ValidationError


class CalculatorForm(ModelForm):
    class Meta:
        model = Calculator
        fields = ('name', 'start_date', 'end_date')
        labels = {
            'name': '계산기 별명',
            'start_date': '입대일',
            'end_date': '전역일',
        }

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if start_date >= end_date:
            raise ValidationError("전역일이 입대일보다 빠를 수 없습니다.")
        else:
            return end_date


class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ('type', 'start_date', 'end_date')
        labels = {
            'type': '종류',
            'start_date': '출발일',
            'end_date': '복귀일',
        }

    def __init__(self, calculator, *args, **kwargs):
        self.calculator = calculator
        super(LeaveForm, self).__init__(*args, **kwargs)

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')

        service_start = self.calculator.start_date
        service_end = self.calculator.end_date

        if service_start <= start_date <= end_date <= service_end:
            return end_date
        else:
            raise ValidationError("휴가기간이 잘못되었습니다.")


class DayoffForm(ModelForm):
    class Meta:
        model = Dayoff
        fields = ('date', 'calculator')
