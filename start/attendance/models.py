from django.db import models
from study.models import Group


class Attend(models.Model):     # 모델폼으로 구현
    attendance = models.ForeignKey(Group, on_delete=models.CASCADE)
    attendance_number = models.CharField(max_length=5, verbose_name='출석확인번호')
    title = models.CharField(max_length=30, verbose_name='출석 제목')
    gather_datetime = models.DateTimeField(verbose_name='모임 날짜와 시간')
    expired_datetime = models.DateTimeField(verbose_name='출석 만료시간')


class AttendConfirm(models.Model):  # 템플릿 인풋으로 폼 구현
    ATTEND_CHANCE = [
        ('지각', '지각'),
        ('출석', '출석')
    ]
    attendconfirm = models.ForeignKey(Attend, on_delete=models.CASCADE)
    attend_user = models.CharField(max_length=20)
    arrive_time = models.DateTimeField()
    sub_time = models.IntegerField()
    attend_check = models.CharField(max_length=20, choices=ATTEND_CHANCE, default='지각')