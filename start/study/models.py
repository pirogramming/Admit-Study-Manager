from django.db import models
from accounts.models import StudyUser
from django.urls import reverse

# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=20, unique=True)
    group_code = models.CharField(max_length=20, unique=True)
    group_member = models.ManyToManyField(StudyUser, through='Membership')

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('study:group_detail', args=[self.id])

class Membership(models.Model):
    person = models.ForeignKey(StudyUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
