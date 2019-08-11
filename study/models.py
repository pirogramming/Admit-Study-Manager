import uuid

from django.db import models
from accounts.models import StudyUser
from django.urls import reverse

# Create your models here.


class Group(models.Model):
    group_name = models.CharField(max_length=20, unique=True)
    group_code = models.CharField(max_length=20)
    invitation_url = models.CharField(max_length=20, unique=True, default=uuid.uuid1)
    group_member = models.ManyToManyField(StudyUser, through='Membership')

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('study:group_detail', args=[self.id])


class Membership(models.Model):
    person = models.ForeignKey(StudyUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('MANAGER', 'MANAGER'),
        ('MEMBER', 'MEMBER')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')

    STATUS_CHOICES = [
        ('NEEDS_APPROVAL', 'NEEDS_APPROVAL'),
        ('ACTIVE', 'ACTIVE'),
        ('OUT', 'OUT')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    # active만 활성화된 유저 - active인 유저들만 가져와서 벌금매기고 등수매기고 해야댐

    @property
    def is_manager(self):
        if self.role == 'MANAGER':
            return True
        else:
            return False