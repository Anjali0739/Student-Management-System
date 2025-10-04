from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),  # /student/
    path("add/", views.add_student, name="add_student"),  # /student/add/
    path("<str:slug>/view/", views.view_student, name="view_student"),  # /student/<slug>/view/
    path("<str:slug>/edit/", views.edit_student, name="edit_student"),  # /student/<slug>/edit/
    path("<str:slug>/delete/", views.delete_student, name="delete_student"),  # /student/<slug>/delete/
]
