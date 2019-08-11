from django.shortcuts import render, get_object_or_404, redirect
from study.models import Group, Membership
from .models import Notice, Homework
from .forms import NoticeForm, HomeworkForm

# Create your views here.


def notice_home(request, id):
    group = get_object_or_404(Group, id=id)
    return render(request, 'studypost/notice_home.html', {
        'group': group,
    })


def notice_new(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            r = request.POST
            notice = Notice.objects.create(group=group, title=r['title'], content=r['content'], lnglat=r['lnglat'])
            lng, lat = map(float, notice.lnglat.split(','))
            return render(request, 'studypost/notice_detail.html', {
                'notice': notice,
                'lng': lng,
                'lat': lat,
            })
    else:
        form = NoticeForm()
    return render(request, 'studypost/notice_new.html', {
        'form': form
    })



def notice_detail(request, id):
    notice = get_object_or_404(Notice, id=id)
    lng, lat = map(float, notice.lnglat.split(','))
    return render(request, 'studypost/notice_detail.html', {
        'notice': notice,
        'lng': lng,
        'lat': lat,
    })


def notice_list(request, id):
    group = Group.objects.get(id=id)
    ns = Notice.objects.filter(group=group)

    return render(request, 'studypost/notice_list.html', {
        'notice_list': ns,
    })


########################################################



def homework_new(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            r = request.POST
            homework = Homework.objects.create(group=group, title=r['title'], content=r['content'])
            return redirect(homework)
    else:
        form = HomeworkForm()
    return render(request, 'studypost/homework_new.html', {
        'form': form
    })


def homework_detail(request, id):
    homework = get_object_or_404(Homework, id=id)

    return render(request, 'studypost/homework_detail.html', {
        'homework': homework,
    })


def homework_list(request, id):
    group = Group.objects.get(id=id)
    hs = Homework.objects.filter(group=group)

    return render(request, 'studypost/homework_list.html', {
        'homework_list': hs,
    })