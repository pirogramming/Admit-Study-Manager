from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'group_code']

class RegisterForm(forms.Form):
    group_name = forms.CharField()
    group_code = forms.CharField()
