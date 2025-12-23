from django.contrib import admin
from .models import Student, Attendance
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "roll_no", "s_class", "email")
    search_fields = ("name", "roll_no", "email")
    list_filter = ("s_class",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "present")
    list_filter = ("date", "present", "student__s_class")
    search_fields = ("student__name", "student__roll_no")
