from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']