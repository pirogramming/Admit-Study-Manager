from django.urls import path

from post import views


urlpatterns = [
    path('<str:group_name>/', views.post)
]