from django.urls import path

from table import views

urlpatterns =[
    path('<int:id>/attendtable', views.attendtable ,name='attendtable')
]