from django.shortcuts import render, redirect
from .forms import SignupForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return redirect('accounts:login')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')