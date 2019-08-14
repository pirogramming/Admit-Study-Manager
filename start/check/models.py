from django.db import models
from study.models import Group


class UpdateHistory(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
