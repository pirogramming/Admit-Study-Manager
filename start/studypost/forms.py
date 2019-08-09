from django import forms
from .models import Notice, Homework


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'
        exclude = ['group']

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = '__all__'
        exclude = ['group']