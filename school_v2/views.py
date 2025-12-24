from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, "v2/dashboard.html")


def students(request):
    return render(request, "v2/students.html")


def mark_attendance(request):
    return render(request, "v2/mark_attendance.html")


def attendance_report(request):
    return render(request, "v2/attendance_report.html")


def attendance_list(request):
    return render(request, "v2/attendance_list.html")
