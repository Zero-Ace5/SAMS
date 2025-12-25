from django.urls import path
from .api_views import StudentListCreateAPI, StudentDetailAPI, AttendanceAPI, AttendanceReportAPI

urlpatterns = [
    path("students/", StudentListCreateAPI.as_view()),
    path("students/<int:pk>/", StudentDetailAPI.as_view()),
    path("attendance/", AttendanceAPI.as_view()),
    path("attendance/report/", AttendanceReportAPI.as_view()),
]
