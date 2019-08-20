from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'group_code']
        labels = {
            'group_name':'스터디 이름',
            'group_code':'스터디 가입용 코드'
        }
        help_texts = {
            'group_code' : '스터디 이름을 검색 후 가입용 코드를 입력하여 스터디에 가입할 수 있습니다!'
        }

class RegisterForm(forms.Form):
    group_code = forms.CharField()

class GroupProfileForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'group_bio', 'group_goal']

        labels = {
            'group_name': '스터디이름',
            'group_bio': '스터디그룹 소개',
            'group_goal': '스터디 목표'
        }

        # help_texts = {}
