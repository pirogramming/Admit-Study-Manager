from django.urls import path

from table import views

app_name = 'table'

urlpatterns =[
    path('<int:id>/attendtable', views.attendtable ,name='table')
]