from django import forms
from widgets.naver_map_point_widget import NaverMapPointWidget
from .models import Notice, Homework



class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'
        exclude = ['group']
        widgets = {
            'lnglat': NaverMapPointWidget,
        }



class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = '__all__'
        exclude = ['group']