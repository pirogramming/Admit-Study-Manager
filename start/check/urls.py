from django.urls import path
from check import views

app_name = 'check'

urlpatterns = [
    path('<int:group_id>/', views.check_home, name="check_home"),
    path('<int:group_id>/update', views.update, name="update"),
]