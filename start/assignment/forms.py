from django import forms
from .models import Assignment, Done


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ['created_at', 'group', 'index_in_group']


class DoneForm(forms.ModelForm):
    class Meta:
        model = Done
        fields = ('done_img',)

