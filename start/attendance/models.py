from datetime import datetime

from django.db import models
from study.models import Group
from accounts.models import StudyUser


class Attend(models.Model):     # 모델폼으로 구현
    ATTEND_STATUS =[
        ('출석 시작 전', '출석 시작 전'),
        ('정상 출석 가능', '정상 출석 가능'),
        ('지각 출석 가능', '지각 출석 가능'),
        ('출석 시간 만료', '출석 시간 만료')
    ]
    attendance = models.ForeignKey(Group, on_delete=models.CASCADE)
    attendance_number = models.CharField(max_length=5, verbose_name='출석확인번호')
    title = models.CharField(max_length=30, verbose_name='출석 제목')
    init_datetime = models.DateTimeField(verbose_name='출석가능 시작시간')
    gather_datetime = models.DateTimeField(verbose_name='모임 날짜와 시간')
    expired_datetime = models.DateTimeField(verbose_name='출석가능 만료시간')
    attend_status = models.CharField(max_length=15, choices=ATTEND_STATUS, default='출석불가')
    attend_data_checked = models.BooleanField(default=False, verbose_name='결석 처리 여부')

    def get_set(self):
        return self.attendconfirm_set.all()

    def attended(self):
        return [x.person for x in AttendConfirm.objects.filter(attend=self, attend_check='출석')]

    def late(self):
        return [x.person for x in AttendConfirm.objects.filter(attend=self, attend_check='지각')]

    def absent(self):
        return [x.person for x in AttendConfirm.objects.filter(attend=self, attend_check='결석')]

    def sub_time(self):
        now_time = datetime.now()
        sub_time = self.expired_datetime - self.gather_datetime
        sub_time = sub_time.seconds//60
        return sub_time


class AttendConfirm(models.Model):  # 템플릿 인풋으로 폼 구현
    ATTEND_CHANCE = [
        ('출석 정보 없음', '출석 정보 없음'),
        ('지각', '지각'),
        ('출석', '출석'),
        ('결석', '결석')
    ]
    attend = models.ForeignKey(Attend, on_delete=models.CASCADE)
    person = models.ForeignKey(StudyUser, on_delete=models.CASCADE)
    attend_user = models.CharField(max_length=20, verbose_name='출석 닉네임')
    arrive_time = models.DateTimeField(null=True, blank=True, verbose_name='도착 시간')
    sub_time = models.IntegerField(null=True, blank=True, verbose_name='시간 차이')
    attend_check = models.CharField(max_length=20, choices=ATTEND_CHANCE, default='없음')