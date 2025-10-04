# teacher/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),  # list all teachers
    path('add/', views.add_teacher, name='add_teacher'),  # add teacher
    path('<int:id>/', views.teacher_detail, name='teacher_detail'),  # view teacher detail
    path('<int:teacher_id>/edit/', views.edit_teacher, name='edit_teacher'),  # edit teacher
]
