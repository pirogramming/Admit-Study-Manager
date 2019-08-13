from django import forms
from django.forms import DateInput
from .models import Attend


class AttendForm(forms.ModelForm):    # attend를 만들어준다

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

    gather_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        label='모임 날짜 선택'
    )
    gather_time_ampm = forms.ChoiceField(label='이번 모임은', choices=AMPM_CHOICES)
    gather_time_hour = forms.ChoiceField(label='시', choices=TIME_CHOICES)
    gather_time_minute = forms.ChoiceField(label='분', choices=MINUTE_CHOICES)
    expired_timedelta = forms.IntegerField(label='분 동안 출석 가능합니다')

    class Meta:
        model = Attend
        fields = ['title', 'attendance_number']
        labels = {
            'title': '제목',
            'attendance_number': '출석 번호 지정',
        }


class AttendConfirmForm(forms.Form):   # 출석을 처리하고 confirm인스턴스 만들기
     input_number = forms.CharField()