from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, StudyUser

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(StudyUser)
class StudyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nickname', 'email', 'phone_number')


