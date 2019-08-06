from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupForm, RegisterForm
from .models import Group, Membership
from django import forms

# Create your views here.


def group_list(request):
    return render(request, 'study/group_list.html', {})


def group_detail(request, id):
    group = get_object_or_404(Group, id=id)

    return render(request, 'study/group_detail.html', {
        'group': group,
    })


def group_new(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
        return redirect(group)
    else:
        form = GroupForm()
    return render(request, 'study/group_form.html', {
        'form': form,
    })


def group_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = request.user
            group = Group.objects.get(group_name=request.POST['group_name'])
            m = Membership.objects.create(person=user, group=group)
        return redirect(group)
    else:
        form = RegisterForm()
    return render(request, 'study/group_register.html', {
        'form': form,
    })


def group_mystudy(request):
    return render(request, 'study/group_mystudy.html')