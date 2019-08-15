from django.urls import path
from . import views

app_name = 'assignment'

urlpatterns = [
    path('<int:group_id>/', views.assignment_home, name='assignment_home'),
    path('<int:group_id>/list/', views.assignment_list, name='assignment_list'),
    path('<int:group_id>/new/', views.assignment_new, name='assignment_new'),
    path('<int:assignment_id>/detail/', views.assignment_detail, name='assignment_detail'),
    path('<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete'),
    path('<int:assignment_id>/edit', views.assignment_edit, name='assignment_edit'),

    path('<int:assignment_id>/done_new/', views.done_new, name='done_new'),
    path('<int:done_id>/done_detail/', views.done_detail, name='done_detail'),
    # path('<int:group_id>/injung_rank/', views.injung_rank, name='injung_rank'),
]