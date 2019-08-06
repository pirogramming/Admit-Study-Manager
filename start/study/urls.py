from django.urls import path
from . import views

app_name = 'study'
urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('new/', views.group_new, name='group_new'),
    path('<int:id>', views.group_detail, name='group_detail'),
    path('register/', views.group_register, name='group_register'),
]