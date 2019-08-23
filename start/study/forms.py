from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'group_code', 'group_bio', 'group_goal']
        labels = {
            'group_name': '',
            'group_code':'',
            'group_bio': '',
            'group_goal': '',
        }

class RegisterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['group_code'].label = ''

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
