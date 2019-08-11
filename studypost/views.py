from django.shortcuts import render, get_object_or_404, redirect
from study.models import Group
from .models import Notice
from .forms import NoticeForm
# Create your views here.


def notice_home(request, id):
    group = get_object_or_404(Group, id=id)
    return render(request, 'studypost/notice_home.html', {
        'group': group,
    })


def notice_new(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save()
            return redirect(notice)
    else:
        form = NoticeForm()
        return render(request, 'studypost/notice_new.html', {'form': form})
    return render(request, 'notice_new.html', {})


def notice_detail(request, id):
    notice = get_object_or_404(Notice, id=id)

    return render(request, 'studypost/notice_detail.html', {
        'notice': notice,
    })


def notice_list(request, id):
    group = Group.objects.get(id=id)
    ns = Notice.objects.filter(group=group)

    return render(request, 'studypost/notice_list.html', {
        'notice_list': ns,
    })