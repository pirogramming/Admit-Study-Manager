from django.db import models
from study.models import Group


class Attend(models.Model):     # 모델폼으로 구현
    attendance = models.ForeignKey(Group, on_delete=models.CASCADE)
    attendance_number = models.CharField(max_length=5)
    title = models.CharField(max_length=30, verbose_name='출석')
    gather_time = models.DateTimeField(verbose_name='모임시간')
    expired_time = models.IntegerField(verbose_name='만료시간')  # 이 시간까지 멤버들 출석 찍기 가능함(지각으로 인정되는 시간)


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