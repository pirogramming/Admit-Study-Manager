from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm, ProfileForm, ProfileImgForm
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
        profileform = ProfileForm(data=request.POST, instance=request.user)
        imageform = ProfileImgForm(data=request.FILES, instance=request.user)
        if profileform.is_valid():
            user = profileform.save()
            return redirect('accounts:profile')
        elif imageform.is_valid():
            user2 = imageform.save()
            return redirect('accounts:profile')
    else:
        profileform = ProfileForm(instance=request.user)
        imageform = ProfileImgForm(instance=request.user)
        forms = {'profileform': profileform, 'imageform': imageform}
        return render(request, 'accounts/profile_revise.html', forms)
