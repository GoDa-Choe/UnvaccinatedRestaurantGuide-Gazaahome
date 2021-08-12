from django.contrib.auth.hashers import check_password
from django import forms


class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if self.user.has_usable_password():
            confirm_password = self.user.password
            if not check_password(password, confirm_password):
                raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
            else:
                return password
        else:
            confirm_email = self.user.email
            if password != confirm_email:
                raise forms.ValidationError("이메일이 일치하지 않습니다.")
            else:
                return password
