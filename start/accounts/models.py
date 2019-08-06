from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(blank=True, max_length=5)
    phone_number = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=50)


class StudyUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('major', '일')
        return super().create_superuser(username, email, password, **extra_fields)


class StudyUser(AbstractUser):
    major = models.CharField(
        max_length=10,
        choices=(
            ('1', '일'),
            ('2', '이'),
            ('3', '삼'),
        )
    )

    objects = StudyUserManager




