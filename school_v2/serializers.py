from rest_framework import serializers
from .models import Student, Attendance


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "roll_no", "s_class", "email"]


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.name",
        read_only=True,
    )

    student_roll = serializers.CharField(
        source="student.roll_no",
        read_only=True,
    )

    class Meta:
        model = Attendance
        fields = ["id", "student", "student_name",
                  "student_roll", "date", "present"]
