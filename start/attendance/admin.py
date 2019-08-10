from django.contrib import admin
from attendance.models import Attend, AttendConfirm


@admin.register(Attend)
class AttendAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'attendance_number', 'gather_time', 'expired_time')


@admin.register(AttendConfirm)
class StudyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'attend_user', 'arrive_time', 'sub_time', 'attend_check')
