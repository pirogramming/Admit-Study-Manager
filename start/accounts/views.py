from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import SignupForm, UserEditForm
from django.contrib.auth.decorators import login_required


# Create your views here.


class UserCreateView(CreateView):
    template_name = 'accounts/signup_form.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')


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