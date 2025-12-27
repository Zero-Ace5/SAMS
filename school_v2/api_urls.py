from django.urls import path
from .api_views import StudentListCreateAPI, StudentDetailAPI, AttendanceAPI, AttendanceReportAPI, StudentAttendanceAPI

urlpatterns = [
    path("students/", StudentListCreateAPI.as_view()),
    path("students/<int:pk>/", StudentDetailAPI.as_view()),
    path("attendance/", AttendanceAPI.as_view()),
    path("attendance/report/", AttendanceReportAPI.as_view()),

    path("student/<int:student_id>/attendance/",
         StudentAttendanceAPI.as_view()),
]
