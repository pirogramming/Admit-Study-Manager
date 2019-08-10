from django.shortcuts import render, get_object_or_404, redirect, resolve_url

from attendance.forms import AttendForm
from study.models import Group
from datetime import  timedelta

# Create your views here.


def time_cal(timedelt):
    if timedelt.days == -1:
        return (86400-timedelt.seconds)//60
    elif timedelt.days == 0:
        return -(timedelt.seconds//60 + 1)


def attend_list(request, group_id):     # 리스트와 디테일 템플릿 거의 동일하게
    group = get_object_or_404(Group, id=group_id)
    posts = group.attend_set.all().order_by('-pk')[:11]
    return render(request, 'attendance/attend_list.html', {'posts': posts, 'group': group})


def attend_detail(request, group_id, detail_id):
    group = get_object_or_404(Group, id=group_id)
    posts = group.attend_set.all().ordered_by('-pk')
    detail = group.attend_set.get(id=detail_id)
    context = {'posts': posts, 'detail': detail}
    return render(request, 'attendance/attend_detail.html', context)
    # 여기서 출석을 처리

    # 현재 attend 모델 인스턴스를 가져온다
    # 인스턴스.attendance_number가 request.post와 같은지 확인한다
    # if 일치할경우 confirm에 인스턴스를 생성하고 저장한다
    # 일치하지 않을 경우 에러 or 메시지를 발생시킨다

    # 출석을 인스턴스를 만들었으면 membership 모델을 불러온다
    # 출석을 했을 경우 membership 모델 안의 admit속성에 ㅇㅈ을 하나 더한다
    # 출석을 안 했을 경우 벌금 definition을 만들어 정해진 기준에 변수를 곱한다
    # 가령 지각횟수 필드 만들어서 지각횟수 x 벌금기준 같은걸 맴버십에 더한다던지
    # membership = Membership.objets.get(person=request.user, group=group)
    # membership.admit += 1
    # membership.save()


def attend_new(request, group_id):
    # 출석 포스트를 만드는 역할
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            gather_time = request.cleaned_data['gather_time']
            expired_time = gather_time + timedelta(minutes=request.cleaned_data['expired_time'])
            group.attend_set.create(
                attendance_number=request.cleaned_data['attendance_number'],
                title=request.cleaned_data['title'],
                gather_time=gather_time,
                expired_time=expired_time,
            )
        return redirect(resolve_url('attendance:list', group_id=group.id))

    else:
        form = AttendForm()
        return render(request, 'attendance/attend_new.html', {'form': form})


def attend_edit(request, group_id, detail_id):   # 출석 포스트 수정
    return render(request, 'attendance/attend_edit.html')


