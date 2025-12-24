from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard),
    path("students/", views.students),
    path("attendance/report/", views.attendance_report),
    path("attendance/mark/", views.mark_attendance),
    path("attendance/", views.attendance_list),
]
