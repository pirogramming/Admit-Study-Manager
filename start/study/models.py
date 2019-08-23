import uuid
from django.db import models
from accounts.models import StudyUser
from django.urls import reverse

# Create your models here


class Group(models.Model):
    group_name = models.CharField(max_length=20, unique=True)
    group_code = models.CharField(max_length=20)
    invitation_url = models.CharField(max_length=20, unique=True, default=uuid.uuid1)
    group_bio = models.CharField(max_length=300, blank=True, null=True, default='그룹 소개를 50자 이내(한줄)로 작성해주세요')
    group_goal = models.CharField(max_length=50, blank=True, null=True, default='그룹 목표를 50자 이내(한줄)로 작성해주세요')
    group_rule = models.CharField(max_length=50, blank=True, null=True, default='그룹 규칙을 작성해주세요')
    late_penalty = models.CharField(max_length=10, default="0")
    abscence_penalty = models.CharField(max_length=10, default="0")
    notsubmit_penalty = models.CharField(max_length=10, default="0")
    group_member = models.ManyToManyField(StudyUser, through='Membership')

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('study:group_detail', args=[self.id])

    def get_members(self):
        return len(Membership.objects.filter(group=self, status='ACTIVE'))


class Membership(models.Model):
    person = models.ForeignKey(StudyUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('MANAGER', 'MANAGER'),
        ('STAFF', 'STAFF'),
        ('MEMBER', 'MEMBER')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')

    STATUS_CHOICES = [
        # ('NEEDS_APPROVAL', 'NEEDS_APPROVAL'),
        ('ACTIVE', 'ACTIVE'),
        ('OUT', 'OUT')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    # 총합 필드
    total_admit = models.IntegerField(default=0, verbose_name='인정 총합')
    total_penalty = models.IntegerField(default=0, verbose_name='벌금 총합')
    # 출석 처리 필드
    penalty_attend = models.IntegerField(default=0, verbose_name='출석 벌금 총합')
    noshow_attend = models.IntegerField(default=0, verbose_name='출석 결석 횟수')
    late_attend = models.IntegerField(default=0, verbose_name='출석 지각 횟수')
    admit_attend = models.IntegerField(default=0, verbose_name='출석 인정')
    # 과제 처리 필드
    penalty_assign = models.IntegerField(default=0, verbose_name='과제 벌금 총합')
    noshow_assign = models.IntegerField(default=0, verbose_name='과제 미제출 횟수')
    admit_assign = models.IntegerField(default=0, verbose_name='과제 인정')
    rank = models.IntegerField(default=0, null=True, verbose_name='등수')

    phone_number_open = models.BooleanField(default = False)
    bio_open = models.BooleanField(default= False)


    @property
    def is_manager(self):
        if self.role == 'MANAGER':
            return True
        else:
            return False

    @property
    def is_staff(self):
        if self.role == 'STAFF':
            return True
        else:
            return False

    @property
    def is_mn_stf(self):
        if self.role == 'MANAGER' or self.role == 'STAFF':
            return True
        else:
            return False

    @property
    def is_active(self):
        if self.status == 'ACTIVE':
            return True
        else:
            return False

    # def is_notself(request, self):
    #     if self == request.user:
    #         return True
    #     else :
    #         False


class UpdateHistory(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True, verbose_name='업데이트 기준')