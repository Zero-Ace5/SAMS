from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard),
    path("students/", views.students),
    path("attendance/report/", views.attendance_report),
    path("attendance/mark/", views.mark_attendance),
    path("attendance/", views.attendance_list),
    path("students/<int:pk>/edit/", views.student_edit),
    path("students/add/", views.student_add),

    path("my/attendance/", views.student_attendance_page),
]
