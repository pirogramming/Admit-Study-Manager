from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from attendance.forms import AttendForm, AttendConfirmForm
from django.urls import reverse
from study.models import Group
from datetime import timedelta, datetime, time


def sub_timedelta_operator(time_delta):
    if time_delta.days == -1:
        return (86400-time_delta.seconds)//60
    elif time_delta.days == 0:
        return -(time_delta.seconds//60 + 1)


def gather_time_hour_processor(time_hour, time_ampm):
    if time_ampm == 'PM':
        gather_time_hour_processed = int(time_hour)+12
    else:
        gather_time_hour_processed = int(time_hour)

    return gather_time_hour_processed


def attend_list(request, group_id):     # 리스트와 디테일 템플릿 거의 동일하게
    group = get_object_or_404(Group, id=group_id)
    posts = group.attend_set.all().order_by('-pk')[:5]
    context = {'posts': posts, 'group': group}
    return render(request, 'attendance/attend_list.html', context)


def attend_detail(request, group_id, detail_id):
    group = get_object_or_404(Group, id=group_id)
    attend = group.attend_set.get(id=detail_id)
    instances = attend.attendconfirm_set.all().order_by('pk')

    # 출석 가능여부 판단
    if attend.init_datetime <= datetime.now() <= attend.expired_datetime:
        attend.attend_status = '출석가능'
        attend.save()
    else:
        attend.attend_status = '출석불가'
        attend.save()

    #출석하기
    if request.method == 'POST':
        form = AttendConfirmForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            input_attend_number = form.cleaned_data['input_number']
            attend_number = attend.attendance_number
            print(input_attend_number)
            print(attend_number)

            if attend_number == input_attend_number:
                state_time = attend.gather_datetime   # 시간처리 시작!
                print(state_time)
                arrive_time = datetime.now()
                print(arrive_time)
                sub_time_arrange = state_time - arrive_time
                print(sub_time_arrange)
                sub_time = sub_time_arrange.seconds     # todo 지금은 timedelta 초인데 분으로 바꿔줘야댐
                print(sub_time)

                attend.attendconfirm_set.create(
                    attend_user=request.user,
                    arrive_time=arrive_time,
                    sub_time=sub_time,
                    attend_check='출석'
                )

                print(attend.attendconfirm_set.all())
                messages.success(request, '성공적으로 출석했습니다!')
                return redirect(reverse(
                    'attendance:detail',
                    kwargs={'group.id': group_id, 'attend.id': detail_id})
                )

            else:
                messages.error(request, '출석 코드가 일치하지 않습니다.')
                return redirect(reverse(
                    'attendance:detail',
                    kwargs={'group.id': group_id, 'attend.id': detail_id})
                )
        else:
            pass    # 비밀번호 밸리데이션 추가하면 여기다가 쓰기
    else:
        form = AttendConfirmForm()
        context = {
            'group': group,
            'attend': attend,
            'form': form,
            'instances': instances,
        }
        return render(request, 'attendance/attend_detail.html', context)


def attend_new(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = AttendForm(request.POST)

        if form.is_valid():
            gather_date = form.cleaned_data['gather_date']

            gather_time = time(
                gather_time_hour_processor(
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

            group.attend_set.create(
                title=form.cleaned_data['title'],
                attendance_number=form.cleaned_data['attendance_number'],
                gather_datetime=gather_datetime,
                init_datetime=init_datetime,
                expired_datetime=expired_datetime,
            )

        return redirect(resolve_url('attendance:attend_list', group_id=group.id))

    else:
        form = AttendForm()
        return render(request, 'attendance/attend_new.html', {'form': form})


def attend_edit(request, group_id, attend_id):   # 출석 포스트 수정
    return render(request, 'attendance/attend_edit.html')


