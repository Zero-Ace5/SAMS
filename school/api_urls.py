from django.urls import path
from .api_views import StudentAPI, StudentDetailAPI, AttendanceAPI

urlpatterns = [
    path("students/", StudentAPI.as_view()),
    path("students/<int:pk>/", StudentDetailAPI.as_view()),
    path("attendance/", AttendanceAPI.as_view()),
]
