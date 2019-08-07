from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupForm, RegisterForm
from .models import Group, Membership
from django.http import HttpResponse
from django.contrib import messages

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
    return render(request, 'study/group_new.html', {
        'form': form,
    })


def group_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = request.user
            name_list = [x.group_name for x in Group.objects.all()]
            name = request.POST['group_name']
            if name in  name_list:
                group = Group.objects.get(group_name=name)
                code_list = [x.group_code for x in Group.objects.all()]
                code = request.POST['group_code']
                if code in code_list:
                    if group == Group.objects.get(group_code=code):
                        m = Membership.objects.create(person=user, group=group)
                    else:
                        messages.success(request, '코드가 일치하지 않습니다.')
                        form = RegisterForm()
                        return render(request, 'study/group_register.html', {
                            'form': form,
                        })
                else:
                    messages.success(request, '존재하지 않는 코드입니다.')
                    form = RegisterForm()
                    return render(request, 'study/group_register.html', {
                        'form': form,
                    })
            else:
                messages.success(request, '존재하지 않는 그룹입니다.')
                form = RegisterForm()
                return render(request, 'study/group_register.html', {
                    'form': form,
                })
        return redirect(group)
    else:
        form = RegisterForm()
    return render(request, 'study/group_register.html', {
        'form': form,
    })


def group_mystudy(request):
    return render(request, 'study/group_mystudy.html')