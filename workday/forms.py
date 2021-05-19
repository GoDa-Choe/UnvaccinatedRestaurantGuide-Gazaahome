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

    # def clean_start_date(self):
    #     end_date = self.cleaned_data.get('end_date')
    #     start_date = self.cleaned_data.get('start_date')
    #     if start_date >= end_date:
    #         raise ValidationError("전역일이 입대일보다 빠를 수 없습니다.")
    #     return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if start_date >= end_date:
            raise ValidationError("전역일이 입대일보다 빠를 수 없습니다.")
        elif (end_date - start_date).days >= 573:
            raise ValidationError("군복무 기간이 18개월을 넘습니다.")

        return end_date


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
