from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("students/", student_list, name="students"),
    path("students/add/", add_student, name="add_student"),
    path("students/<int:pk>/delete/", delete_student, name="delete_student"),
    path("students/<int:pk>/edit/", edit_student, name="edit_student"),
    path("attendance/mark/", mark_attendance, name="mark_attendance"),
    path("attendance/", attendance_list, name="attendance_list"),
    path("attendance/report/", attendance_report, name="attendance_report"),

]
