from django.contrib import admin
from .models import Group, Membership

# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'group_code']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['person', 'group']