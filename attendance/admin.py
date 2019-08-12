from django.contrib import admin
from attendance.models import Attend, AttendConfirm


@admin.register(Attend)
class AttendAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'attendance_number', 'gather_datetime', 'expired_datetime')


@admin.register(AttendConfirm)
class StudyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'attend_user', 'arrive_time', 'sub_time', 'attend_check')
