from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from attendance.forms import AttendForm, AttendConfirmForm
from study.models import Group, Membership
from datetime import timedelta, datetime, time
from attendance.models import Attend
from study.models import Membership


def sub_timedelta_function(time_delta):
    if time_delta.days == -1:
        return (86400 - time_delta.seconds) // 60
    elif time_delta.days == 0:
        return -(time_delta.seconds // 60 + 1)


def gather_time_hour_function(time_hour, time_ampm):
    if time_ampm == 'PM':
        gather_time_hour_processed = int(time_hour) + 12
    else:
        gather_time_hour_processed = int(time_hour)
    return gather_time_hour_processed


def attend_status_function(now_time, init_time, state_time, expired_time):
    if now_time < init_time:
        status = '출석 시작 전'
    elif init_time <= now_time <= state_time:
        status = '정상 출석 가능'
    elif state_time <= now_time <= expired_time:
        status = '지각 출석 가능'
    elif expired_time < now_time:
        status = '출석 시간 만료'
    return status


def attend_list(request, group_id):  # 리스트와 디테일 템플릿 거의 동일하게
    group = get_object_or_404(Group, id=group_id)
    posts = group.attend_set.all().order_by('-pk')[:5]
    for post in posts:
        post.attend_status = attend_status_function(
            datetime.now(),
            post.init_datetime,
            post.gather_datetime,
            post.expired_datetime
        )
        post.save()
    context = {'posts': posts, 'group': group}
    return render(request, 'attendance/attend_list.html', context)


def attend_detail(request, group_id, detail_id):
    group = get_object_or_404(Group, id=group_id)
    attend = group.attend_set.get(id=detail_id)
    membership = group.membership_set.get(person=request.user)

    if request.method == 'POST':
        form = AttendConfirmForm(request.POST)

        # 중복 출석 방지
        confirm_value = attend.attendconfirm_set.filter(
            attend_user=request.user.nickname,
            attend_check='출석 정보 없음'
        )

        if confirm_value:
            if form.is_valid():
                input_attend_number = form.cleaned_data['input_number']
                attend_number = attend.attendance_number

                if attend_number == input_attend_number:

                    # 결석 인스턴스 가져오기
                    attending_member = attend.attendconfirm_set.get(attend_user=request.user.nickname)

                    # 시간처리
                    state_time = attend.gather_datetime
                    arrive_time = datetime.now()
                    sub_time_arrange = state_time - arrive_time
                    sub_time = sub_timedelta_function(sub_time_arrange)

                    # 지각, 출석 기록
                    if attend.attend_status == '정상 출석 가능':
                        attending_member.arrive_time = arrive_time
                        attending_member.sub_time = sub_time
                        attending_member.attend_check = '출석'
                        attending_member.save()
                        membership.admit_attend += 1    # ㅇㅈ하나 추가
                        membership.save()
                        messages.success(request, '성공적으로 출석했습니다!')
                        return redirect(resolve_url('attendance:attend_detail', group.id, attend.id))

                    elif attend.attend_status == '지각 출석 가능':
                        attending_member.arrive_time = arrive_time
                        attending_member.sub_time = sub_time
                        attending_member.attend_check = '지각'
                        attending_member.save()
                        membership.late_attend += 1    # 지각 횟수 한번 추가
                        membership.save()
                        messages.success(request, '지각입니다ㅜㅜ')
                        return redirect(resolve_url('attendance:attend_detail', group.id, attend.id))

                else:
                    messages.error(request, '출석 코드가 일치하지 않습니다')
                    return redirect(resolve_url('attendance:attend_detail', group.id, attend.id))
            else:
                messages.error(request, '출석 코드에는 숫자만 입력해주세요')
                return redirect(resolve_url('attendance:attend_detail', group.id, attend.id))
        else:
            messages.error(request, '이미 출석하셨습니다')
            return redirect(resolve_url('attendance:attend_detail', group.id, attend.id))
    else:
        instances_attend = attend.attendconfirm_set.filter(attend_check='출석').order_by('arrive_time')
        instances_late = attend.attendconfirm_set.filter(attend_check='지각').order_by('arrive_time')
        instances_none = attend.attendconfirm_set.filter(attend_check='출석 정보 없음')
        instances_absence = attend.attendconfirm_set.filter(attend_check='결석')
        form = AttendConfirmForm()
        context = {
            'group': group,
            'attend': attend,
            'form': form,
            'instances_attend': instances_attend,
            'instances_late': instances_late,
            'instances_none': instances_none,
            'instances_absence': instances_absence,
        }
        return render(request, 'attendance/attend_detail.html', context)


def attend_new(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_members = group.membership_set.all()

    if request.method == 'POST':
        form = AttendForm(request.POST)

        if form.is_valid():
            gather_date = form.cleaned_data['gather_date']

            gather_time = time(
                gather_time_hour_function(
                    form.cleaned_data['gather_time_hour'],
                    form.cleaned_data['gather_time_ampm']
                ),
                int(form.cleaned_data['gather_time_minute'])
            )

            gather_datetime = datetime.combine(gather_date, gather_time)
            init_datetime = gather_datetime - timedelta(minutes=60)
            expired_datetime = gather_datetime + timedelta(
                minutes=form.cleaned_data['expired_timedelta']
            )

            new_attend = group.attend_set.create(
                title=form.cleaned_data['title'],
                attendance_number=form.cleaned_data['attendance_number'],
                gather_datetime=gather_datetime,
                init_datetime=init_datetime,
                expired_datetime=expired_datetime,
            )

            for member in group_members:
                new_attend.attendconfirm_set.create(
                    attend_user=member.person.nickname,
                    attend_check='출석 정보 없음'
                )

        return redirect(resolve_url('attendance:attend_list', group_id=group.id))

    else:
        form = AttendForm()
        return render(request, 'attendance/attend_new.html', {'form': form})


def attend_edit(request, detail_id):
    attend = get_object_or_404(Attend, id=detail_id)
    group = attend.attendance
    membership = Membership.objects.get(person=request.user, group=group)

    if request.method == 'POST':
        form = AttendForm(request.POST, instance=attend)
        if form.is_valid():
            attend = form.save()
            return render(request, 'attendance/attend_detail.html', {
                'attend': attend,
                'membership': membership,
            })
    else:
        form = AttendForm(instance=attend)
    return render(request, 'attendance/attend_new.html', {
        'form': form,
    })


def attend_delete(request, detail_id):
        attend = get_object_or_404(Attend, id=detail_id)
        group = attend.attendance
        membership = Membership.objects.get(person=request.user, group=group)
        attend.delete()

        posts = group.attend_set.all().order_by('-pk')[:5]

        return render(request, 'attendance/attend_list.html', {
            'group': group,
            'posts': posts,
            'membership': membership,
        })

