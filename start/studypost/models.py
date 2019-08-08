from django.db import models
from django.urls import reverse
from start.study.models import Group


<<<<<<< HEAD
class GroupPost(models.Model):
    group_post = models.ForeignKey(Group, on_delete=models.CASCADE)
=======

class Notice(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
>>>>>>> b4f58291db5c571b02bf6ccdf0a867c776f9bf08
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse('studypost:notice_detail', args=[self.id])
