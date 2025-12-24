from django.urls import path
from .api_views import StudentListCreateAPI, StudentDetailAPI, AttendanceAPI

urlpatterns = [
    path("students/", StudentListCreateAPI.as_view()),
    path("students/<int:pk>/", StudentDetailAPI.as_view()),
    path("attendance/", AttendanceAPI.as_view()),
]
