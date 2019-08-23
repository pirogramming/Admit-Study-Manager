from django import forms
from django.forms import DateInput

from .models import Assignment, Done


class AssignmentForm(forms.ModelForm):

    AMPM_CHOICES = (
        ('', '오전오후'),
        ('AM', '오전'),
        ('PM', '오후')
    )

    TIME_CHOICES = (
        ('', '시각을 고르세요'),
        (1, '1'), (2, '2'), (3, '3'), (4, '4'),
        (5, '5'), (6, '6'), (7, '7'), (8, '8'),
        (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    MINUTE_CHOICES = (
        ('', '분을 고르세요'),
        (0, '00'), (5, '05'), (10, '10'), (15, '15'),
        (20, '20'), (25, '25'), (30, '30'), (35, '35'),
        (40, '40'), (45, '45'), (50, '50'), (55, '55'),
    )

    due_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        label='날짜'
    )
    due_date_ampm = forms.ChoiceField(label='이번 과제는', choices=AMPM_CHOICES)
    due_date_hour = forms.ChoiceField(label='시', choices=TIME_CHOICES)
    due_date_minute = forms.ChoiceField(label='분', choices=MINUTE_CHOICES)

    class Meta:
        model = Assignment
        fields = ['title', 'content']
        labels = {
            'title': '과제명',
            'content': '내용',
        }


class DoneForm(forms.ModelForm):
    class Meta:
        model = Done
        fields = ('done_img',)
        labels = {
            'done_img': '이미지 첨부',
        }


