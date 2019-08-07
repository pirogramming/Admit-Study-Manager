from random import randint

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import LoginForm
from accounts.models import StudyUser
from .forms import GroupForm, RegisterForm
from .models import Group, Membership
from django.contrib import messages

# Create your views here.


def all_group_list(request):
    gs = Group.objects.all()
    g = request.GET.get('g', '')

    if g:
        gs = gs.filter(group_name__icontains=g)

    return render(request, 'study/all_group_list.html', {
        'all_group_list': gs,
    })

def group_list(request):
    user = request.user
    group_list = Group.objects.filter(group_member=user)
    g = request.GET.get('g', '')
    if g:
        group_list = group_list.filter(group_name__icontains=g)

    return render(request, 'study/group_list.html', {
        'group_list': group_list
    })


def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    membership = [x.person for x in Membership.objects.filter(group=group)]

    return render(request, 'study/group_detail.html', {
        'group': group, 'membership':membership,
    })


def group_new(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            name = request.POST['group_name']
            name_list = [x.group_name for x in Group.objects.all()]
            if name not in name_list:
                group = form.save(commit=False)
                while True:
                    try:
                        group.invitation_url = str(randint(1, 999999)).zfill(6)
                        group.save()
                        break
                    except:
                        pass
                group.save()
                m = Membership.objects.create(person=request.user, group=group)
                messages.success(request, '새 그룹을 만들었습니다')
                return redirect(group)
            else:
                messages.error(request, '이미 존재하는 그룹입니다.')
                form = GroupForm()
                return render(request, 'study/group_new.html', {
                    'form': form,
                })

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
            if name in name_list:
                group = Group.objects.get(group_name=name)
                code_list = [x.group_code for x in Group.objects.all()]
                code = request.POST['group_code']
                if code in code_list:
                    if group == Group.objects.get(group_name=name, group_code=code):
                        for x in Membership.objects.all():
                            if str(user) == str(x.person) and str(name) == str(x.group):
                                messages.error(request, '이미 가입되었습니다.')
                                form = RegisterForm()
                                return render(request, 'study/group_register.html', {
                                    'form': form,
                                })

                        m = Membership.objects.create(person=user, group=group)
                        messages.success(request, '그룹에 가입되었습니다.')
                        return redirect(group)
                    else:
                        messages.error(request, '코드가 일치하지 않습니다.')
                        form = RegisterForm()
                        return render(request, 'study/group_register.html', {
                            'form': form,
                        })
                else:
                    messages.error(request, '존재하지 않는 코드입니다.')
                    form = RegisterForm()
                    return render(request, 'study/group_register.html', {
                        'form': form,
                    })
            else:
                messages.error(request, '존재하지 않는 그룹입니다.')
                form = RegisterForm()
                return render(request, 'study/group_register.html', {
                    'form': form,
                })
    else:
        form = RegisterForm()
    return render(request, 'study/group_register.html', {
        'form': form,
    })


def group_registerbyurl(request, invitation_url):
    group = Group.objects.get(invitation_url=invitation_url)
    membership = [x.person for x in Membership.objects.filter(group=group)]
    user = request.user
    if request.method == 'POST':
        try:
            if user not in membership:
                m = Membership.objects.create(person=user, group=group)
                messages.success(request, '"{}"그룹 가입을 축하합니다!'.format(group.group_name))
                return redirect(group)

            else:
                return render(request, 'study/group_registerbyurl_fail.html')

        except:
            form = LoginForm(request.POST)
            id = request.POST['username']
            pw = request.POST['password']
            u = authenticate(username=id, password=pw)

            if u:
                login(request, user=u)
                return render(request, 'study/group_registerbyurl.html', {'group': group,
                                                                          'form': form,
                                                                          'membership':membership})
            else:
                return render(request, 'study/group_registerbyurl.html', {'group': group,
                                                                          'form': form,
                                                                          'error':'아이디나 비밀번호가 일치하지 않습니다.',
                                                                          'membership':membership})

                # return render(request, 'study/group_registerbyurl.html', {'group':group})

    else :
        group = Group.objects.get(invitation_url=invitation_url)
        form = LoginForm()
        return render(request, 'study/group_registerbyurl.html', {'group':group,
                                                                  'form':form,
                                                                  'membership':membership})


def group_mystudy(request):
    return render(request, 'study/group_mystudy.html')

def mystudy_list(request,id):
    user = get_object_or_404(StudyUser,id=id)
    groups = Membership.objects.filter(person=user)

    return render(request, 'study/mystudy_list.html',{
        'user': user, 'groups': groups,
    })