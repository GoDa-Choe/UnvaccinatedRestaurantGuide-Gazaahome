from workday.models import Calculator, Leave, Dayoff
from django.forms import ModelForm, ValidationError, Form, TextInput
from django.forms import CharField

SEARCH_ATTRS = {
    "placeholder": "친구 계산기 별명",
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


class CalculatorForm(ModelForm):
    class Meta:
        model = Calculator
        fields = ('name', 'start_date', 'end_date', 'is_open')
        labels = {
            'name': '계산기 별명',
            'start_date': '입대일',
            'end_date': '전역일',
            'is_open': '검색 허용',
        }

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if start_date >= end_date:
            raise ValidationError("전역일이 입대일보다 빠를 수 없습니다.")
        else:
            return end_date


class CalculatorSettingsForm(ModelForm):
    class Meta:
        model = Calculator
        fields = ('name', 'is_open')
        labels = {
            'name': '계산기 별명',
            'is_open': '검색 허용',
        }


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
