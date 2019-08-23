from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import StudyUser


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['email'].label = '이메일*'

        self.fields['password1'].help_text = "8자 이상, 영문 숫자 특수문자를 섞어주세요"
        self.fields['password2'].help_text = "비밀번호를 한번 더 입력해주세요"
        self.fields['username'].help_text = "8자 이상, 영문/숫자만 가능합니다"

    class Meta(UserCreationForm.Meta):
        model = StudyUser
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'nickname',
            'phone_number'
        ]

        labels = {
            'username': '아이디',
            'email': '이메일',
            'nickname': '닉네임',
            'phone_number': '전화번호',
        }
        help_texts = {
            'email': ('이메일 형식에 맞게 적어주세요'),
            'nickname': ('다섯자 이하로 입력하세요'),
            'phone_number': ('"-" 를 포함해서 입력해주세요')
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

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['password'].label = '비밀번호'
        self.fields['username'].help_text = " "

    class Meta:
        model = StudyUser
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password']


class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['img_profile'].label = ''


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
            'nickname': '5자 이하로 써주세요',
            'phone_number': '"-"를 포함해서 써주세요',
            'bio': '자신을 소개해주세요',
        }
