import random
from datetime import datetime, time
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from attendance.views import gather_time_hour_function
from study.models import Group, Membership
from .models import Assignment, Done, Injung_history
from .forms import AssignmentForm, DoneForm
from study.views import manager_required, mn_stf_required



def assignment_home(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    usermembership = Membership.objects.get(group=group, person=request.user)
    assignments = Assignment.objects.filter(group=group).order_by('-created_at')[:5]
    dones = Done.objects.filter(assignment__group=group).order_by('-created_at')[:5]
    now = datetime.now()

    ctx = {
        'group': group, 'usermembership': usermembership, 'assignments': assignments, 'dones': dones, 'now': now,
    }
    return render(request, 'assignment/assignment_home.html', ctx)


def assignment_list(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    usermembership = Membership.objects.get(group=group, person=request.user)
    assignments = Assignment.objects.filter(group=group).order_by('-created_at')
    num = len(assignments)
    now = datetime.now()
    return render(request, 'assignment/assignment_list.html', {
        'group': group, 'assignments': assignments, 'num': num, 'now': now,
        'usermembership':usermembership,
    })



def assignment_new(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    usermembership = Membership.objects.get(group=group, person=request.user)
    if Membership.objects.get(group=group, person=request.user).role == 'MEMBER':
        messages.warning(request, '매니저와 스탭만 과제를 등록할 수 있습니다.')
        return redirect('assignment:assignment_list', group_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.group = group
            assignment.index_in_group = len(Assignment.objects.filter(group=group)) + 1

            date = form.cleaned_data['due_date']

            due_time = time(
                gather_time_hour_function(
                    form.cleaned_data['due_date_hour'],
                    form.cleaned_data['due_date_ampm']
                ),
                int(form.cleaned_data['due_date_minute'])
            )

            due_date = datetime.combine(date, due_time)

            assignment.due_date = due_date
            assignment.save()
            return redirect(assignment)

    else:
        form = AssignmentForm()
        return render(request, 'assignment/assignment_new.html',
                      {'form': form, 'group':group,
                       'usermembership':usermembership})


def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    group = assignment.group
    assignments = Assignment.objects.filter(group=group).order_by('-created_at')
    user = request.user
    usermembership = Membership.objects.get(group=group, person=request.user)
    membership = Membership.objects.get(person=user, group=group)
    dones = Done.objects.filter(assignment=assignment)
    authors = [x.author for x in dones]
    now = datetime.now()

    ctx = {'assignment': assignment, 'assignments': assignments,
        'group': group, 'dones': dones, 'authors': authors,
          'num': len(dones), 'usermembership': usermembership, 'membership': membership,
          'now': now, 'user': user, }
    return render(request, 'assignment/assignment_detail.html', ctx)


def done_new(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    group = assignment.group
    usermembership = Membership.objects.get(group=group, person=request.user)
    if datetime.now() >= assignment.due_date:
        messages.warning(request, '제출기한이 지났습니다.')
        return redirect('assignment:assignment_detail', assignment_id)
    elif request.method == 'POST':
        form = DoneForm(request.POST, request.FILES)
        if form.is_valid():
            done = form.save(commit=False)
            done.author = request.user
            done.assignment = assignment
            done.index_in_assignment = len(Done.objects.filter(assignment=assignment))+1
            done.save()
            return redirect(done)
    else:
        form = DoneForm()
        return render(request, 'assignment/done_new.html', {
            'form': form, 'assignment': assignment,
        'group':group,
        'usermembership':usermembership,})


def done_list(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    dones = Done.objects.filter(assignment__group=group).order_by('-created_at')
    ctx = {'group': group, 'dones': dones, }
    return render(request, 'assignment/done_list.html', ctx)


def done_detail(request, done_id):
    done = get_object_or_404(Done, id=done_id)
    group = done.assignment.group
    usermembership = Membership.objects.get(group=group, person=request.user)

    return render(request, 'assignment/done_detail.html', {
        'group':group,
        'done': done,
        'usermembership':usermembership,
    })


def injung_plus(request, done_id):
    done = get_object_or_404(Done, id=done_id)
    original_author = Membership.objects.get(person=done.author, group=done.assignment.group)
    injungs = Injung_history.objects.filter(done=done)
    authors = [x.author for x in injungs]

    if done.author == request.user:
        messages.warning(request, "너무 잘하시긴 했어요.. 그렇지만 자신의 과제에는 인정을 누를 수 없습니다.")
        return redirect(done)
    elif request.user in authors:
        when = injungs.get(author=request.user).created_at
        messages.warning(request, "이미 {}에 인정하셨습니다!".format(when))
        return redirect(done)
    else:
        done.injung += 1
        original_author.admit_assign += 1
        original_author.total_admit += 1
        done.save()
        original_author.save()
        new_injung = Injung_history.objects.create(author=request.user, done=done,)

        memberships = Membership.objects.filter(group=done.assignment.group)
        for m in memberships:
            m.rank = 1
            for mc in memberships:
                if m.total_admit < mc.total_admit:
                    m.rank += 1
            m.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def assignment_edit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    group = assignment.group
    usermembership = Membership.objects.get(group=group, person=request.user)


    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            date = form.cleaned_data['due_date']

            due_time = time(
                gather_time_hour_function(
                    form.cleaned_data['due_date_hour'],
                    form.cleaned_data['due_date_ampm']
                ),
                int(form.cleaned_data['due_date_minute'])
            )

            due_date = datetime.combine(date, due_time)

            assignment.due_date = due_date
            assignment.save()
            return redirect(assignment)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignment/assignment_new.html', {
        'group':group,
        'form': form,
        'usermembership':usermembership,
    })



def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    group = assignment.group
    usermembership = Membership.objects.get(group=group, person=request.user)
    assignment.delete()

    assignment = Assignment.objects.filter(group=group).order_by('created_at').last()
    done = Done.objects.filter(assignment=assignment).order_by('created_at').last()

    return render(request, 'assignment/assignment_home.html', {
        'assignment': assignment,
        'done': done,
        'group': group,
        'usermembership':usermembership,
    })


'''
def admit_rank(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    memberships = Membership.objects.filter(group=group)
    users = [x.person for x in memberships]
    injung_rank = []

    for user in users:
        dones = Done.objects.filter(author=user)
        total_injung = sum([int(x.injung) for x in dones])
        injung_rank.append(total_injung)

    injung_rank.sort(reverse=True)

    while True:
        random.shuffle(users)
        injung_rank2 = []
        for user in users:
            dones = Done.objects.filter(author=user)
            total_injung = sum([int(x.injung) for x in dones])
            injung_rank2.append(total_injung)

        if injung_rank == injung_rank2:
            break
        else:
            continue


    return render(request, 'assignment/injung_rank.html', {
        'user_list': users,
    })
'''
