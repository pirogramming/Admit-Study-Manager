from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.utils.html import format_html
from study.models import Group, Membership
from attendance.models import Attend, AttendConfirm
from assignment.models import Assignment


def attendtable(request, id):
    group = get_object_or_404(Group, id=id)
    user =request.user
    usermembership = get_object_or_404(Membership, person=user, group=group)
    attends = Attend.objects.filter(attendance=group)

    assignments = Assignment.objects.filter(group=group)


    memberships = Membership.objects.filter(group=group, status='ACTIVE')

    ctx = {
        'group':group,
        'usermembership':usermembership,
        'attends':attends,
        'assignments':assignments,

        'memberships':memberships,
    }
    return render(request, 'table/table.html', ctx)