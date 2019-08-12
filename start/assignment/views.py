from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from study.models import Group, Membership
from .models import Assignment, Done
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
    return render(request, 'assignment/assignment_list.html', {
        'group': group, 'assignments': assignments, 'num': num,
    })


def assignment_new(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if not Membership.objects.get(group=group, person=request.user).is_manager:
        messages.warning(request, '매니저만 과제를 등록할 수 있습니다.')
        return redirect('assignment:assignment_list', group_id)
    else:
        if request.method == 'POST':
            form = AssignmentForm(request.POST)
            if form.is_valid():
                assignment = form.save(commit=False)
                assignment.group = group
                assignment.index_in_group = len(Assignment.objects.filter(group=group))+1
                assignment.save()
                return redirect(assignment)
        else:
            form = AssignmentForm()
            return render(request, 'assignment/assignment_new.html', {'form': form})


def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    dones = Done.objects.filter(assignment=assignment)
    authors = [x.author for x in dones]
    return render(request, 'assignment/assignment_detail.html', {
        'assignment': assignment, 'dones': dones, 'authors': authors, 'num': len(dones),
    })


def done_new(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
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
