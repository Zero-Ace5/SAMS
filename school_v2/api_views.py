from datetime import date
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Student, Attendance
from .serializers import StudentSerializer, AttendanceSerializer


class StudentListCreateAPI(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, requesr, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendanceAPI(APIView):
    def get(self, request):
        date_param = request.GET.get("date")
        if not date_param:
            date_param = date.today().isoformat()

        records = Attendance.objects.filter(date=date_param)
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        date_value = request.data.get("date")
        records = request.data.get("records", [])

        if not date_value or not isinstance(records, list):
            return Response(
                {"error": "Invalid Data Entered"},
                status=status.HTTP_404_NOT_FOUND,
            )

        saved = []

        with transaction.atomic():
            for item in records:
                student_id = item.get("student")
                present = item.get("present", True)

                student = Student.objects.get(pk=student_id)

                attendance, _ = Attendance.objects.update_or_create(
                    student=student,
                    date=date_value,
                    defaults={"present": present},
                )

                saved.append(attendance)

        serializer = AttendanceSerializer(saved, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
