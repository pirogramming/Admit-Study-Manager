from datetime import datetime
import functools
from random import randint
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from accounts.forms import LoginForm
from accounts.models import StudyUser
from assignment.models import Assignment, Done
from attendance.views import attend_status_function
from .forms import GroupForm, RegisterForm, GroupProfileForm
from .models import Group, Membership, UpdateHistory
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


def mn_stf_required(func):
    @functools.wraps(func)
    def wrapper(request, id):
        group = get_object_or_404(Group, id=id)
        group_name = group.group_name
        user = request.user
        membership = Membership.objects.get(group=group, person=user)
        if not membership.is_mn_stf or not membership.is_active:
            # return render(request, 'study/group_reject.html', {'group_name': group_name})
            return HttpResponse("매니저 권한이 필요합니다.")
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

    groups = [x.group.group_name for x in Membership.objects.filter(person=user, status='ACTIVE')]
    gs = Group.objects.filter(group_name__in=groups)
    g = request.GET.get('g', '')
    if g:
        gs = gs.filter(group_name__icontains=g)

    return render(request, 'study/group_list.html', {
        'group_list': gs,
    })


def all_group_detail(request,id):
    group = get_object_or_404(Group, id=id)
    # membership_manager = [x.person for x in Membership.objects.filter(group=group, role='MANAGER', status='ACTIVE')]
    # membership_member = [x.person for x in Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')]

    membership_manager = Membership.objects.filter(group=group, role='MANAGER', status='ACTIVE')
    membership_staff = Membership.objects.filter(group=group, role='STAFF', status='ACTIVE')
    membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')

    return render(request, 'study/all_group_detail.html', {
        'group': group,
        'membership_manager': membership_manager,
        'membership_staff': membership_staff,
        'membership_member': membership_member,
    })


@group_required
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    user = request.user
    # membership = [x.person for x in Membership.objects.filter(group=group)]
    membership_manager = Membership.objects.filter(group=group, role='MANAGER', status='ACTIVE')
    membership_staff = Membership.objects.filter(group=group, role='STAFF', status='ACTIVE')
    membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')
    usermembership = Membership.objects.get(group=group, person=user)

    memberships = Membership.objects.filter(group=group).order_by('-total_admit')
    penalty_list = Membership.objects.filter(group=group).order_by('-total_penalty')

    latest_update = UpdateHistory.objects.filter(group=group).order_by('created_at').last()
    attend_posts = group.attend_set.all().order_by('-pk')[:3]
    notice_posts = group.notice_set.all().order_by('-pk')[:3]
    assign_posts = group.assignment_set.filter(group=group).order_by('-pk')[:3]

    for post in attend_posts:
        post.attend_status = attend_status_function(
            datetime.now(),
            post.init_datetime,
            post.gather_datetime,
            post.expired_datetime
        )
        post.save(update_fields=['attend_status'])

    context = {
        'membership_manager': membership_manager,
        'membership_staff': membership_staff,
        'membership_member': membership_member,
        'usermembership': usermembership,
        'group': group,
        'memberships_zip': zip(memberships, range(1, (len(memberships)+1))),
        'penalty_list_zip': zip(penalty_list, range(1, (len(penalty_list)+1))),
        'latest_update': latest_update,
        'attend_posts': attend_posts,
        'notice_posts': notice_posts,
        'assign_posts': assign_posts
    }

    return render(request, 'study/group_detail.html', context)


@group_required
def group_update(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    memberships = Membership.objects.filter(group=group).order_by('-total_admit')
    members = [x.person for x in memberships]

    # 과제 미제출 처리
    assignments = Assignment.objects.filter(done_checked=False, group=group, due_date__lte=datetime.now())
    for assignment in assignments:
        dones = Done.objects.filter(assignment=assignment)
        submitters = [x.author for x in dones]
        assignment.done_checked = True
        assignment.save(update_fields=['done_checked'])
        for member in members:
            if member not in submitters:
                non_submit = memberships.get(person=member)
                non_submit.noshow_assign = non_submit.noshow_assign + 1
                non_submit.save()

    # 결석 처리

    attends = group.attend_set.filter(attend_status='출석 시간 만료', attend_data_checked=False)
    for attend in attends:
        instances = attend.attendconfirm_set.filter(attend_check='출석 정보 없음')
        for instance in instances:
            instance.attend_check = '결석'
            instance.save(update_fields=['attend_check'])
            absense_membership = group.membership_set.get(person=instance.person)
            absense_membership.noshow_attend += 1
            absense_membership.save(update_fields=['noshow_attend'])
        attend.attend_data_checked = True
        attend.save(update_fields=['attend_data_checked'])

    # 업데이트 기록 저장
    UpdateHistory.objects.create(group=group, created_at=datetime.now())

    # 벌금 산출 함수로 넘어가기
    return redirect(resolve_url('study:penalty', group.id))


def penalty(request, id):
    group = Group.objects.get(id=id)
    memberships = Membership.objects.filter(group=group)
    for membership in memberships:
        penalty_attend = membership.late_attend * int(group.late_penalty) + \
                         membership.noshow_attend * int(group.abscence_penalty)
        penalty_assign = int(group.notsubmit_penalty) * membership.noshow_assign
        membership.penalty_attend = penalty_attend
        membership.penalty_assign = penalty_assign
        membership.total_penalty = penalty_attend + penalty_assign
        membership.save(update_fields=['penalty_attend', 'penalty_assign', 'total_penalty'])
    return redirect(resolve_url('study:group_detail', group.id))


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
        'user': user,
        'group': group,
        'membership': usermembership,
    })

@group_required
@manager_required
def group_settings_mn(request, id):
    user = request.user
    group = get_object_or_404(Group.objects.prefetch_related(), id=id)
    membership_manager = Membership.objects.filter(group=group, role='MANAGER', status='ACTIVE')
    membership_staff = Membership.objects.filter(group=group, role='STAFF', status='ACTIVE')
    membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')
    groupprofileform = GroupProfileForm(instance=group)

    ctx = {'user': user, 'group': group,
           'groupprofileform': groupprofileform,
           'membership_manager': membership_manager,
           'membership_staff': membership_staff,
           'membership_member': membership_member,
           }

    if request.method == 'POST':
        if request.POST.get('groupprofilerevise', ''):
            groupprofileform = GroupProfileForm(request.POST, request.FILES, instance=group)
            if groupprofileform.is_valid():
                us = groupprofileform.save()
                ctx['groupprofileform'] = groupprofileform
                # messages.success(request, '그룹 프로필을 성공적으로 수정했습니다.')
                return render(request, 'study/group_settings_mn.html', ctx)
                # return redirect('study:group_settings', id)

        elif request.POST.get('rulerevise', ''):
            group_rule = request.POST.get('group_rule', '')
            late_penalty = request.POST.get('late_penalty', '')
            abscence_penalty = request.POST.get('abscence_penalty', '')
            notsubmit_penalty = request.POST.get('notsubmit_penalty', '')

            group.group_rule = group_rule
            group.late_penalty = late_penalty
            group.abscence_penalty = abscence_penalty
            group.notsubmit_penalty = notsubmit_penalty
            group.save()

            return render(request, 'study/group_settings_mn.html', ctx)

        elif request.POST.get('staffout', ''):
            out_staffname = request.POST['staffout']
            out_staff = get_object_or_404(StudyUser, username=out_staffname)
            obj = get_object_or_404(Membership, person=out_staff, group=group)
            obj.role = 'MEMBER'
            obj.save()
            membership_staff = Membership.objects.filter(group=group, role='STAFF', status='ACTIVE')
            membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')
            ctx['membership_staff'] = membership_staff
            ctx['membership_member'] = membership_member
            return render(request, 'study/group_settings_mn.html', ctx)

        elif request.POST.get('staffin', ''):
            for i in range(1, len(membership_member) + 1):
                try:
                    in_staffname = request.POST['staffin{}'.format(i)]
                    in_staff = get_object_or_404(StudyUser, username=in_staffname)
                    obj = get_object_or_404(Membership, person=in_staff, group=group)
                    obj.role = 'STAFF'
                    obj.save()
                except:
                    pass
            membership_staff = Membership.objects.filter(group=group, role='STAFF', status='ACTIVE')
            membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')
            ctx['membership_staff'] = membership_staff
            ctx['membership_member'] = membership_member
            return render(request, 'study/group_settings_mn.html', ctx)

        elif request.POST.get('managerin', ''):
            # print(request.POST.get('managerin', ''))
            manager_username = request.POST.get('managerin', '')
            manager_user = get_object_or_404(StudyUser, username=manager_username)
            obj = get_object_or_404(Membership, person=manager_user, group=group)
            obj.role = 'MANAGER'
            obj.save()
            ect = get_object_or_404(Membership, person=user, group=group)
            ect.role = 'MEMBER'
            ect.save()
            messages.success(request, '관리자 권한을 위임했습니다.')
            return redirect(group)

        elif request.POST['out']:
            # if request.POST.get('out', '') :
            # Membership.objects.get(person=user, group=group).update(status='OUT')
            out_username = request.POST['out']
            out_user = get_object_or_404(StudyUser, username=out_username)
            obj = get_object_or_404(Membership, person=out_user, group=group)
            obj.status = 'OUT'
            obj.save()
            return redirect(group)

        else:
            return render(request, 'study/group_settings_mn.html', ctx)

        return redirect(group)

    return render(request, 'study/group_settings_mn.html', ctx)

@group_required
@mn_stf_required
def group_settings_stf(request, id):
    user = request.user
    group = get_object_or_404(Group.objects.prefetch_related(), id=id)
    membership_manager = Membership.objects.filter(group=group, role='MANAGER', status='ACTIVE')
    membership_staff = Membership.objects.filter(group=group, role='STAFF', status='ACTIVE')
    membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')
    groupprofileform = GroupProfileForm(instance=group)

    ctx = {'user': user, 'group': group,
           'groupprofileform': groupprofileform,
           'membership_manager': membership_manager,
           'membership_staff': membership_staff,
           'membership_member': membership_member,
           }

    if request.method == 'POST':
        if request.POST.get('groupprofilerevise', ''):
            groupprofileform = GroupProfileForm(request.POST, request.FILES, instance=group)
            if groupprofileform.is_valid():
                us = groupprofileform.save()
                ctx['groupprofileform'] = groupprofileform
                # messages.success(request, '그룹 프로필을 성공적으로 수정했습니다.')
                return render(request, 'study/group_settings_stf.html', ctx)
                # return redirect('study:group_settings', id)

        elif request.POST.get('rulerevise', ''):
            group_rule = request.POST.get('group_rule', '')
            late_penalty = request.POST.get('late_penalty', '')
            abscence_penalty = request.POST.get('abscence_penalty', '')
            notsubmit_penalty = request.POST.get('notsubmit_penalty', '')

            group.group_rule = group_rule
            group.late_penalty = late_penalty
            group.abscence_penalty = abscence_penalty
            group.notsubmit_penalty = notsubmit_penalty
            group.save()

            return render(request, 'study/group_settings_stf.html', ctx)
        elif request.POST.get('staffin', ''):
            for i in range(1, len(membership_member) + 1):
                try:
                    in_staffname = request.POST['staffin{}'.format(i)]
                    in_staff = get_object_or_404(StudyUser, username=in_staffname)
                    obj = get_object_or_404(Membership, person=in_staff, group=group)
                    obj.role = 'STAFF'
                    obj.save()
                    membership_staff = Membership.objects.filter(group=group, role='STAFF', status='ACTIVE')
                    membership_member = Membership.objects.filter(group=group, role='MEMBER', status='ACTIVE')
                    ctx['membership_staff'] = membership_staff
                    ctx['membership_member'] = membership_member
                except:
                    pass

            return render(request, 'study/group_settings_stf.html', ctx)

        elif request.POST['out']:
            # if request.POST.get('out', '') :
            # Membership.objects.get(person=user, group=group).update(status='OUT')
            out_username = request.POST['out']
            out_user = get_object_or_404(StudyUser, username=out_username)
            obj = get_object_or_404(Membership, person=out_user, group=group)
            obj.status = 'OUT'
            obj.save()
            return redirect(group)

        else:
            return render(request, 'study/group_settings_stf.html', ctx)

        return redirect(group)

    return render(request, 'study/group_settings_stf.html', ctx)


def group_base(request, id):
    group = get_object_or_404(Group.objects.prefetch_related(), id=id)
    user = request.user
    ctx = {
        'group':group,
        'user':user,
    }
    return render(request, 'group_base.html', ctx)

def member_info(request, id):
    group = get_object_or_404(Group, id=id)
    membership = get_object_or_404(Membership, id=id)
    user = membership.person

    return render(request, 'study/member_info.html', {
        'group':group,
        'user': user,
        'membership': membership,
    })


def member_info_list(request, id):
    group = get_object_or_404(Group, id=id)
    memberships = Membership.objects.filter(group=group)

    return render(request, 'study/member_info_list.html', {
        'group':group,
        'memberships': memberships
    })


