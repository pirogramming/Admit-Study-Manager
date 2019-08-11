from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import StudyUser, Profile


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = StudyUser
        fields = ['username',
                  'password1',
                  'password2',
                  'email',
                  'nickname',
                  'phone_number'
                  ]

        labels = {
            'username': '아이디',
            'password': '비밀번호',
            'email': '이메일',
            'nickname': '닉네임',
            'phone_number': '전화번호',
        }
        help_texts = {
            'password' : (''),
            'nickname': ('다섯자 이하로 입력하세요'),
            'phone_number' : ('"-" 를 포함해서 입력해주세요')
        }

    def saved(self):
        user = super().save()
        StudyUser.objects.create(
            user=user,
            nickname=self.cleaned_data['nickname'],
            phone_number=self.cleaned_data['phone_number'],
        )
        return user


class LoginForm(forms.ModelForm):
    class Meta:
        model = StudyUser
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password']
        labels = {
            'username': '아이디',
            'password': '비밀번호',
        }


class UserEditForm(UserChangeForm):
    class Meta:
        model = StudyUser
        fields = ['img_profile', 'nickname', 'phone_number', 'bio']

        labels = {
            'nickname': '사용자이름',
            'phone_number': '전화번호',
            'img_profile': '프로필 사진',
            'bio': '자기소개',
        }

        help_texts = {
            'phone_number': '"-"를 포함해서 써주세요'
        }
