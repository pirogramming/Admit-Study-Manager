import re
from django.forms import ValidationError
from django.db import models
from django.urls import reverse
from study.models import Group
from accounts.models import StudyUser



def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid LngLat Type')


class Notice(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    lnglat = models.CharField(max_length=50, blank=True,
                              validators=[lnglat_validator],
                              verbose_name='장소')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(StudyUser, on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('studypost:notice_detail', args=[self.id])


class Homework(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(StudyUser, on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('studypost:homework_detail', args=[self.id])



