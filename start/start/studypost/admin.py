from django.contrib import admin
from .models import Notice

# Register your models here.


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass