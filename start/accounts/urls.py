from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name ='accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login_form.html'), name='login'),
    path('profile/', views.profile, name='profile'),
]