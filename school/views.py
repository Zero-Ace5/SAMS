import requests
from django.shortcuts import render, redirect
from datetime import date
# Create your views here.

API_BASE = "http://127.0.0.1:8000/api"


def dashboard(request):
    today = date.today().isoformat()

    students = requests.get(f"{API_BASE}/students/").json()

    attendance = requests.get(f"{API_BASE}/attendance/?date={today}").json()

    present_students = {a["student"] for a in attendance if a["present"]}

    present = len(present_students)
    absent = len(students) - present

    return render(request, "dashboard.html", {
        "attendance_date": today,
        "total_students": len(students),
        "present": present,
        "absent": absent,
    })


def student_list(request):
    response = requests.get(f"{API_BASE}/students/")
    students = response.json()
    return render(request, "students.html", {"students": students})


def add_student(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "roll_no": request.POST.get("roll_no"),
            "s_class": request.POST.get("s_class"),
            "email": request.POST.get("email"),
        }

        response = requests.post(f"{API_BASE}/students/", json=data)

        if response.status_code == 201:
            return redirect("/students/")
        return render(request, "add_student.html", {
            "errors": response.json()
        })

    return render(request, "add_student.html")


def delete_student(request, pk):
    requests.delete(f"{API_BASE}/students/{pk}/")
    return redirect("/students/")


def edit_student(request, pk):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "roll_no": request.POST.get("roll_no"),
            "s_class": request.POST.get("s_class"),
            "email": request.POST.get("email"),
        }

        response = requests.put(f"{API_BASE}/students/{pk}/", json=data)

        if response.status_code == 200:
            return redirect("/students/")

        return render(request, "edit_student.html", {
            "errors": response.json()
        })
    student = requests.get(f"{API_BASE}/students/{pk}/").json()
    return render(request, "edit_student.html", {"student": student})


def mark_attendance(request):
    students = requests.get(f"{API_BASE}/students/").json()
    attendance = requests.get(f"{API_BASE}/attendance/").json()

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    attendance_map = {
        a["student"]: a["present"]
        for a in attendance
        if a["date"] == today_str
    }

    for s in students:
        s["present"] = attendance_map.get(s["id"], True)

    if request.method == "POST":
        for s in students:
            present = f"present_{s['id']}" in request.POST
            requests.post(f"{API_BASE}/attendance/", json={
                "student": s["id"],
                "present": present
            })
        return redirect("/attendance/mark/")

    return render(request, "mark_attendance.html", {"students": students, "attendance_date": today, })


def attendance_list(request):
    students = requests.get(f"{API_BASE}/students/").json()
    attendance = requests.get(f"{API_BASE}/attendance/").json()

    selected_date = request.GET.get("date") or date.today().isoformat()

    attendance_map = {
        a["student"]: a["present"]
        for a in attendance
        if a["date"] == selected_date
    }

    for s in students:
        s["present"] = attendance_map.get(s["id"], False)

    return render(request, "attendance_list.html", {
        "students": students,
        "selected_date": selected_date,
    })


def attendance_report(request):
    students = requests.get(f"{API_BASE}/students/").json()
    attendance = requests.get(f"{API_BASE}/attendance/").json()

    selected_date = request.GET.get("date") or date.today().isoformat()

    records_for_date = [
        a for a in attendance if a["date"] == selected_date
    ]

    present = sum(1 for a in records_for_date if a["present"])
    absent = len(students) - present

    return render(request, "attendance_report.html", {
        "selected_date": selected_date,
        "total_students": len(students),
        "present": present,
        "absent": absent,
    })
