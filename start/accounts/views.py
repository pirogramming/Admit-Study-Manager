from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .forms import SignupForm, UserEditForm, LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/signup_form.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')
    success_message = '회원가입 성공! 로그인해주세요'


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('study:mystudy')
        else:
            messages.error(request,'아이디나 비밀번호를 확인해주세요')
            return redirect('accounts:login')

    else:
        form = LoginForm()
    return render(request, 'accounts/login_form.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_revise(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            us = form.save()
            return redirect("accounts:profile")
    else:
        profileform = UserEditForm(instance=request.user)
        forms = {'profileform': profileform}
        return render(request, 'accounts/profile_revise.html', forms)


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, '비밀번호가 변경되었습니다.')
            return redirect('accounts:profile')
        else:
            messages.error(request, '오류를 수정해주세요.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {
        'form': form
    })