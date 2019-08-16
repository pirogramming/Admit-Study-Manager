import uuid
from django.db import models
from accounts.models import StudyUser
from django.urls import reverse

# Create your models here.


class Group(models.Model):
    group_name = models.CharField(max_length=20, unique=True)
    group_code = models.CharField(max_length=20)
    invitation_url = models.CharField(max_length=20, unique=True, default=uuid.uuid1)

    group_bio = models.CharField(max_length=300, blank=True, null=True)
    group_goal = models.CharField(max_length=300, blank=True, null=True)


    group_rule = models.CharField(max_length=600, blank=True, null=True)
    late_penalty = models.CharField(max_length=10, default="0")
    abscence_penalty = models.CharField(max_length=10, default="0")
    notsubmit_penalty = models.CharField(max_length=10, default="0")


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
    total_admit = models.IntegerField(default=0)
    total_penalty = models.IntegerField(default=0)
    attend_admit = models.IntegerField(default=0)
    assign_admit = models.IntegerField(default=0)
    rank = models.IntegerField(default=1)

    phone_number_open = models.BooleanField(default = False)
    bio_open = models.BooleanField(default= False)

    @property
    def phone_number_open(self):
        if self.phone_number_open == True:
            return True
        else:
            return False

    @property
    def bio_open(self):
        if self.bio_open == True:
            return True
        else:
            return False

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
