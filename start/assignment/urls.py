from django.urls import path
from . import views

app_name = 'assignment'

urlpatterns = [
    path('<int:group_id>/new/', views.assignment_new, name='assignment_new'),
    path('<int:id>/', views.assignment_detail, name='assignment_detail'),

    path('<int:assignment_id>/done_new/', views.done_new, name='done_new'),
    path('<int:id>/done_detail/', views.done_detail, name='done_detail'),

]