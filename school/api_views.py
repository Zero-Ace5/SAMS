from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Attendance
from .serializers import StudentSerializer, AttendanceSerializer
from datetime import date
from django.shortcuts import get_object_or_404


class StudentAPI(APIView):  # Handles both list -get and create -post
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AttendanceAPI(APIView):   # Handles both list -get and create -post
    def get(self, request):
        records = Attendance.objects.all()
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        student_id = request.data.get("student")
        present = request.data.get("present", True)

        student = get_object_or_404(Student, pk=student_id)
        today = date.today()

        attendance, created = Attendance.objects.update_or_create(
            student=student,
            date=today,
            defaults={"present": present}
        )

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=201)


class StudentDetailAPI(APIView):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return Response(status=204)
