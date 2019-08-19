import mimetypes
import os
import urllib

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from study.models import Group, Membership
from .models import Notice, Homework
from .forms import NoticeForm, HomeworkForm
from study.views import group_required, manager_required, mn_stf_required


# Create your views here.

@group_required
def notice_home(request, id):
    group = get_object_or_404(Group, id=id)
    usermembership = get_object_or_404(Membership, group=group, person=request.user)

    return render(request, 'studypost/notice_home.html', {
        'group': group,
        'usermembership':usermembership,
    })

@group_required
@mn_stf_required
def notice_new(request, id):
    group = get_object_or_404(Group, id=id)
    usermembership = get_object_or_404(Membership, group=group, person=request.user)

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            r = request.POST
            notice = Notice.objects.create(group=group, title=r['title'],
                                           content=r['content'], lnglat=r['lnglat'],
                                           author=request.user,
                                           photo=request.FILES.get('photo', None),
                                           file=request.FILES.get('file', None)
                                           )
            lng, lat = map(float, notice.lnglat.split(','))
            return render(request, 'studypost/notice_detail.html', {
                'group': group,
                'notice': notice,
                'lng': lng,
                'lat': lat,
                'usermembership':usermembership,
            })
    else:
        form = NoticeForm()
    return render(request, 'studypost/notice_new.html', {
        'group':group,
        'form': form,
        'usermembership':usermembership,
    })



def notice_detail(request, id):
    notice = get_object_or_404(Notice, id=id)
    group = notice.group
    lng, lat = map(float, notice.lnglat.split(','))
    return render(request, 'studypost/notice_detail.html', {
        'notice': notice,
        'lng': lng,
        'lat': lat,
        'group':group,
    })


def notice_list(request, id):
    group = get_object_or_404(Group, id=id)
    ns = Notice.objects.filter(group=group)

    return render(request, 'studypost/notice_list.html', {
        'notice_list': ns,
        'group': group,
    })


def notice_edit(request, id):
    notice = get_object_or_404(Notice, id=id)
    group = notice.group

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            notice = form.save()
            return redirect(notice)
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'studypost/notice_new.html', {
        'form': form,
        'group':group,
    })


def notice_delete(request, id):
    notice = get_object_or_404(Notice, id=id)
    group = notice.group
    usermembership = get_object_or_404(Membership, group=group, person=request.user)

    notice.delete()

    ns = Notice.objects.filter(group=group)

    return render(request, 'studypost/notice_list.html', {
        'group': group,
        'notice_list': ns,
        'usermembership':usermembership,
    })


########################################################



def homework_new(request, id):
    group = Group.objects.get(id=id)
    usermembership = get_object_or_404(Membership, group=group, person=request.user)

    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            r = request.POST
            homework = Homework.objects.create(group=group, title=r['title'],
                                               content=r['content'], author=request.user,
                                               photo=request.FILES.get('photo', None),
                                               file=request.FILES.get('file', None))
            return redirect(homework)
    else:
        form = HomeworkForm()
    return render(request, 'studypost/homework_new.html', {
        'group': group,
        'form': form,
        'usermembership':usermembership,
    })


def homework_detail(request, id):

    homework = get_object_or_404(Homework, id=id)
    group = homework.group

    usermembership = get_object_or_404(Membership, group=group, person=request.user)

    return render(request, 'studypost/homework_detail.html', {
        'group': group,
        'homework': homework,
        'usermembership':usermembership,
    })



def homework_list(request, id):
    group = Group.objects.get(id=id)
    usermembership = get_object_or_404(Membership, group=group, person=request.user)

    hs = Homework.objects.filter(group=group)

    return render(request, 'studypost/homework_list.html', {
        'group': group,
        'homework_list': hs,
        'usermembership': usermembership,
    })


def homework_edit(request, id):

    homework = get_object_or_404(Homework, id=id)

    group = homework.group
    usermembership = get_object_or_404(Membership, group=group, person=request.user)


    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES, instance=homework)
        if form.is_valid():
            homework = form.save()
            return redirect(homework)
    else:
        form = HomeworkForm(instance=homework)
    return render(request, 'studypost/homework_new.html', {
        'group': group,
        'form': form,
        'usermembership':usermembership,
    })



def homework_delete(request, id):
    homework = get_object_or_404(Homework, id=id)
    group = homework.group
    usermembership = get_object_or_404(Membership, group=group, person=request.user)

    homework.delete()

    hs = Homework.objects.filter(group=group)

    return render(request, 'studypost/homework_list.html', {
        'group': group,
        'homework_list': hs,
        'usermembership':usermembership,
    })


def file_download(request, file_path):
    original_filename = file_path.split('\\')[-1]

    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response
