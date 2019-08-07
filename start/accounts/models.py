from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class StudyUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('major', '직장인')
        return super().create_superuser(username, email, password, **extra_fields)


class StudyUser(AbstractUser):
    nickname = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(blank=True, max_length=20, null=True)
    img_profile = models.ImageField(upload_to='user', blank=True, null=True, default=None)
    bio = models.TextField(blank=True, null=True)

    objects = StudyUserManager

    def __str__(self):
        return self.username




