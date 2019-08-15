from django.shortcuts import render, get_object_or_404

from check.models import UpdateHistory
from study.models import Group


def check_home(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if len(UpdateHistory.objects.filter(group=group))==0:
        return render(request, 'check/not_updated.html', {
            'group': group,
        })
    else:
        return render(request, 'check/check_home.html', {
            'group': group,
        })


def update(request, group_id):
    pass
