import re
from django import forms
from .models import User, Article
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['posted_date', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = False
        self.fields['publish'].required = False
        self.fields['views'].required = False

class SignUpForm(forms.Form):
    email = forms.EmailField(label="이메일", widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호", "autocomplete": "new-password"}))
    password_confirm = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인", "autocomplete": "new-password"}))

    def clean(self):
        
        cleaned_data = super(SignUpForm, self).clean()
        
        email = cleaned_data.get("email")

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        match = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        validation = re.compile(match)
        
        if User.objects.filter(email=email).last():
            raise ValidationError({"email": "이미 존재하는 아이디입니다."})
        elif validation.match(str(password)) is None:
            raise ValidationError({"password": "비밀번호는 하나 이상의 문자, 숫자, 특수문자를 포함하여 8자리 이상으로 작성해주세요."})
        elif validation.match(str(password_confirm)) is None:
            raise ValidationError({"password_confirm": "비밀번호는 하나 이상의 문자, 숫자, 특수문자를 포함하여 8자리 이상으로 작성해주세요."})
        elif password and password_confirm:
            if password != password_confirm:
                raise ValidationError({"password": "비밀번호가 일치하지 않습니다."})

class LoginForm(forms.Form):
    email = forms.EmailField(label="이메일", widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호", "autocomplete": "new-password"}))

    
    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user = User.objects.filter(email=email).last()

        if not user:
            raise ValidationError({"email": "올바른 이메일 주소를 입력해주세요."})

        elif not user.is_active:
            raise ValidationError({"email": "탈퇴한 회원입니다."})

        elif not check_password(password, user.password):
            raise ValidationError({"password": "잘못된 비밀번호입니다. 다시 확인하세요."})

        return cleaned_data