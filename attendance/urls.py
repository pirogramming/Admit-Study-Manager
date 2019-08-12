from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views

app_name = 'attendance'

urlpatterns = [
    path('<int:group_id>/', views.attend_list, name='attend_list'),
    path('<int:group_id>/detail/<int:detail_id>', views.attend_detail, name='attend_detail'),
    path('<int:group_id>/new/', views.attend_new, name='attend_new'),
    path('<int:group_id>/edit', views.attend_edit, name='attend_edit'),
]


