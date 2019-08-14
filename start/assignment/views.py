from datetime import datetime, time

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from attendance.views import gather_time_hour_function
from study.models import Group, Membership
from .models import Assignment, Done, Injung_history
from .forms import AssignmentForm, DoneForm


def assignment_home(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    assignment = Assignment.objects.filter(group=group).order_by('created_at').last()
    done = Done.objects.filter(assignment=assignment).order_by('created_at').last()
    return render(request, 'assignment/assignment_home.html', {
        'group': group, 'assignment': assignment, 'done': done,
    })


def assignment_list(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    assignments = Assignment.objects.filter(group=group).order_by('-created_at')
    num = len(assignments)
    now = datetime.now()
    return render(request, 'assignment/assignment_list.html', {
        'group': group, 'assignments': assignments, 'num': num, 'now': now,
    })


def assignment_new(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if not Membership.objects.get(group=group, person=request.user).is_manager:
        messages.warning(request, '매니저만 과제를 등록할 수 있습니다.')
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
        return render(request, 'assignment/assignment_new.html', {'form': form})


def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    group = assignment.group
    user = request.user
    membership = Membership.objects.get(person=user, group=group)

    dones = Done.objects.filter(assignment=assignment)
    authors = [x.author for x in dones]
    now = datetime.now()
    return render(request, 'assignment/assignment_detail.html', {
        'assignment': assignment,
        'dones': dones,
        'authors': authors,
        'num': len(dones),
        'membership': membership,
    })


def done_new(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
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
        return render(request, 'assignment/done_new.html', {'form': form, 'assignment': assignment, })


def done_detail(request, done_id):
    done = get_object_or_404(Done, id=done_id)
    return render(request, 'assignment/done_detail.html', {
        'done': done,
    })



def injung_plus(request, done_id):
    done = get_object_or_404(Done, id=done_id)
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
        done.save()
        new_injung = Injung_history.objects.create(author=request.user, done=done,)
        return redirect(done)


def assignment_edit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save()
            return redirect(assignment)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignment/assignment_new.html', {
        'form': form,
    })


def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    group = assignment.group
    assignment.delete()

    assignment = Assignment.objects.filter(group=group).order_by('created_at').last()
    done = Done.objects.filter(assignment=assignment).order_by('created_at').last()

    return render(request, 'assignment/assignment_home.html', {
        'assignment': assignment,
        'done': done,
        'group': group,
    })

