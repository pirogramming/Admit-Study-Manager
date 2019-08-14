from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'group_code']

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
