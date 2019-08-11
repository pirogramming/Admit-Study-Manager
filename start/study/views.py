import functools
from random import randint

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import LoginForm
from accounts.models import StudyUser

from .forms import GroupForm, RegisterForm
from .models import Group, Membership
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

from study.models import Membership

def group_required(func):
   @functools.wraps(func)
   def wrapper(request, id):
       group = get_object_or_404(Group, id=id)
       group_name = group.group_name
       user = request.user
       usergroup_list = [x.group.group_name for x in Membership.objects.filter(person=user, status='ACTIVE')]
       if request.user.is_authenticated and group_name not in usergroup_list:
           return render(request, 'study/group_reject.html', {'group_name':group_name})
           # return HttpResponse("{}그룹 멤버가 아니므로 글을 쓸 수 없습니다.".format(group_name))

       return func(request, id)
   return wrapper


def manager_required(func):
    @functools.wraps(func)
    def wrapper(request, id):
        group = get_object_or_404(Group, id=id)
        group_name = group.group_name
        user = request.user
        membership = Membership.objects.get(group=group, person=user)
        if not membership.is_manager or not membership.is_active:
            # return render(request, 'study/group_reject.html', {'group_name': group_name})
            return HttpResponse("매니저 권한이 필요합니다.")
        return func(request, id)
    return wrapper


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
    # usergroup_list = [x.group.group_name for x in Membership.objects.filter(person=user, status='ACTIVE')]
    # group_list = Group.objects.filter(group_member=user)
    group_list = [x.group for x in Membership.objects.filter(person = user, status='ACTIVE')]
    g = request.GET.get('g', '')
    if g:
        group_list = group_list.filter(group_name__icontains=g)

    return render(request, 'study/group_list.html', {
        'group_list': group_list
    })


def all_group_detail(request,id):
    group = get_object_or_404(Group, id=id)
    membership = [x.person for x in Membership.objects.filter(group=group, status='ACTIVE')]

    return render(request, 'study/all_group_detail.html', {
        'group': group,
        'membership': membership,
    })

@group_required
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    user = request.user
    # membership = [x.person for x in Membership.objects.filter(group=group)]
    membership_manager = Membership.objects.filter(group=group, role='MANAGER')
    membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')
    usermembership = Membership.objects.get(group=group, person=user)

    return render(request, 'study/group_detail.html', {
        'group': group,
        'membership_manager':membership_manager, 'membership_member':membership_member,
        'usermembership':usermembership,
    })



@login_required
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
                m = Membership.objects.create(person=request.user, group=group, role='MANAGER')
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


def group_register(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = request.user
            name_list = [x.group_name for x in Group.objects.all()]
            name = group.group_name
            if name in name_list:
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
                    messages.error(request, '코드가 일치하지 않습니다.')
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
        'group': group,
    })

@login_required
def group_registerbyurl(request, invitation_url):
    group = Group.objects.get(invitation_url=invitation_url)
    membership = Membership.objects.filter(group=group, status='ACTIVE')
    memberlist = [x.person for x in Membership.objects.filter(group=group)]
    user = request.user
    if request.method == 'POST':
        # try:
        if user not in memberlist:
            m = Membership.objects.create(person=user, group=group)
                # obj = Membership.objects.create(person=user, group=group)
                # obj.status = 'ACTIVE'
                # obj.save()
            messages.success(request, '"{}"그룹에 가입했습니다!'.format(group.group_name))
            return redirect(group)

        else:
            return render(request, 'study/group_registerbyurl_fail.html')

        # except:
        #     form = LoginForm(request.POST)
        #     id = request.POST['username']
        #     pw = request.POST['password']
        #     u = authenticate(username=id, password=pw)

            # if u:
            #     login(request, user=u)
            #     return render(request, 'study/group_registerbyurl.html', {'group': group, 'form': form, 'membership':membership})
            # else:
            #     return render(request, 'study/group_registerbyurl.html', {'group': group, 'form': form, 'error':'아이디나 비밀번호가 일치하지 않습니다.', 'membership':membership})
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
    groups = Membership.objects.filter(person=user, status='ACTIVE')

    return render(request, 'study/mystudy_list.html',{
        'user': user, 'groups': groups,
    })

@login_required
@group_required
def group_mysettings(request, id):
    user = request.user
    group = Group.objects.get(id=id)
    usermembership = Membership.objects.get(person=user, group=group)
    if request.method == 'POST':
        if request.POST.get('out', '') == 'out':
            # Membership.objects.get(person=user, group=group).update(status='OUT')
            obj = Membership.objects.get(person=user, group=group)
            obj.status = 'OUT'
            obj.save()
            return redirect('home')
        return redirect(group)

    return render(request, 'study/group_mysettings.html', {
        'user':user, 'group':group
    })

# @manager_required (매니저만 들어갈 수 있도록 decorator 추가할 예정)
@group_required
@manager_required
def group_settings(request, id):
    user = request.user
    group = Group.objects.get(id=id)
    return render(request, 'study/group_settings.html', {
        'user':user, 'group':group,
    })