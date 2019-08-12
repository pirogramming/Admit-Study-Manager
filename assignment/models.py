from django.db import models
from django.conf import settings
from django.urls import reverse

from study.models import Group


class Assignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    index_in_group = models.IntegerField()
    title = models.CharField(max_length=30, verbose_name='과제명')
    content = models.TextField(verbose_name='내용')
    due_date = models.DateTimeField(verbose_name='기한')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('assignment:assignment_detail', args=[self.id])


class Done(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    index_in_assignment = models.IntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    done_img = models.ImageField(upload_to='AssignmentsDone')
    injung = models.IntegerField(default=0)
    noinjung = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('assignment:done_detail', args=[self.id])
