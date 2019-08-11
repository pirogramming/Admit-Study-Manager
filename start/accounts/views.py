from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

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
