from django.db import models
from django.urls import reverse
from study.models import Group

# Create your models here.


class Notice(models.Model):
    notice = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('studypost:notice_detail', args=[self.id])