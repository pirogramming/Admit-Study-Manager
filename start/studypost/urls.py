from django.urls import path
from . import views
app_name= 'studypost'

urlpatterns = [
    path('notice/<int:id>', views.notice_home, name='notice_home'),
    path('notice_new/', views.notice_new, name='notice_new'),
    path('<int:id>/', views.notice_detail, name='notice_detail'),
    path('notice_list/<int:id>/', views.notice_list, name='notice_list'),
]