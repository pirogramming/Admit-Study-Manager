from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect

from assignment.models import Done, Assignment

from check.models import UpdateHistory
from study.models import Group, Membership


def check_home(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    memberships = Membership.objects.filter(group=group).order_by('-total_admit')
    penalty_list = memberships.order_by('-total_penalty')
    latest_update = UpdateHistory.objects.filter(group=group).order_by('created_at').last()

    if len(UpdateHistory.objects.filter(group=group)) == 0:
        return render(request, 'check/not_updated.html', {
            'group': group,
        })
    else:
        return render(request, 'check/check_home.html', {
            'group': group, 'memberships': memberships, 'penalty_list': penalty_list, 'latest_update': latest_update,
        })


def update(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    memberships = Membership.objects.filter(group=group).order_by('-total_admit')
    members = [x.person for x in memberships]

    # 과제 미제출 반영
    assignments = Assignment.objects.filter(done_checked=False, group=group, due_date__lte=datetime.now())
    for assignment in assignments:
        dones = Done.objects.filter(assignment=assignment)
        submitters_id = [x.author.id for x in dones]
        assignment.done_checked = True
        assignment.save(update_fields=['done_checked'])
        for member in members:
            if member.id not in submitters_id:
                non_submit = memberships.get(person=member, group=group)
                non_submit.noshow_assign += 1
                non_submit.save(update_fields=['noshow_assign'])

    # 결석 반영


    # 위 사항들을 반영한 벌금 산출

    for m in memberships:
        m.total_penalty = int(group.abscence_penalty) * m.noshow_attend + \
                          int(group.late_penalty) * m.late_attend + int(group.notsubmit_penalty) * m.noshow_assign
        m.save(update_fields=['total_penalty'])

    # 업데이트 기록 저장
    new_update = UpdateHistory.objects.create(group=group)

    return redirect('check:check_home', group_id=group.id)










