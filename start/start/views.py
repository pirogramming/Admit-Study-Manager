from django.shortcuts import redirect


def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    else:
        return redirect('study:mystudy')
