from django.urls import path
from . import views

app_name = 'study'
urlpatterns = [
    path('all_group_list', views.all_group_list, name='all_group_list'),
    path('group_list', views.group_list, name='group_list'),
    path('mystudy/', views.group_mystudy, name='mystudy'),
    path('new/', views.group_new, name='group_new'),
    path('<int:id>', views.group_detail, name='group_detail'),
    path('register/', views.group_register, name='group_register'),
    path('invitation/<int:invitation_url>', views.group_registerbyurl, name='group_registerbyurl'),
]