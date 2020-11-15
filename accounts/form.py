from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
from accounts.models import Profile
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ["username", "email"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Profile.objects.filter(email=email)
        if qs:
            raise forms.ValidationError("이미 등록된 이메일 입니다.")
        else:
            return email


class PasswordChangeForm(AuthPasswordChangeForm):

    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        password2 = self.cleaned_data.get('new_password2')
        if old_password and password2:
            if old_password == password2:
                raise forms.ValidationError("전과 동일한 비밀번호를 입력하셨습니다.")
        return password2


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user_photo", "first_name",
                  "last_name", "gender", "phone_number", "addr"]
