from datetime import date
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Student, Attendance
from .serializers import StudentSerializer, AttendanceSerializer

from django.db.models import Count, Q, F

from django.core.cache import cache  # Added Cache

import os
import logging

logger = logging.getLogger(__name__)


class StudentListCreateAPI(APIView):
    def get(self, request):
        # added v1 meaning version 1. for tracking.
        cache_key = "student:list:v1"
        data = cache.get(cache_key)

        if data is None:
            logger.warning("CACHE MISS → DB QUERY - 1")
            # students = Student.objects.all()
            # data = StudentSerializer(students, many=True).data
            students = Student.objects.values(
                "id", "name", "roll_no", "s_class", "email")
            data = list(students)
            cache.set(cache_key, data, 600)
        else:
            logger.warning("CACHE HIT - 1")

        return Response(data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # This line below will invalidate a existing cache on every new record addition
            cache.delete("student:list")
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

    def delete(self, request, pk):
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

        # records = (Attendance.objects.filter(date=date_param).annotate(
        #     student_name=F("student__name"),
        #     student_roll=F("student__roll_no"),).values(
        #     "student_name",
        #     "student_roll",
        #     "present",
        # ))

        # return Response(list(records))

    def post(self, request):
        date_value = request.data.get("date")
        records = request.data.get("records", [])

        if not date_value or not isinstance(records, list):
            return Response(
                {"error": "Invalid Data Entered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        saved = []

        with transaction.atomic():
            for item in records:
                student_id = item.get("student")
                present = item.get("present", True)

                student = get_object_or_404(Student, pk=student_id)

                attendance, _ = Attendance.objects.update_or_create(
                    student=student,
                    date=date_value,
                    defaults={"present": present},
                )
                # cache invalidation for the StudentAttendanceAPI
                cache.delete(f"attendance:student:{student.id}")
                # cache.delete_pattern("attendance:student:*")
                saved.append(attendance)

        cache.delete("student:list")
        serializer = AttendanceSerializer(saved, many=True)
        # print("PID:", os.getpid())
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttendanceReportAPI(APIView):
    def get(self, request):
        total_students = Student.objects.count()

        report = (
            Attendance.objects.values("date").annotate(
                present=Count("id", filter=Q(present=True)),).order_by("-date")
        )

        result = []

        for r in report:
            result.append({
                "date": r["date"],
                "present": r["present"],
                "absent": total_students - r["present"],
            })

        return Response(result)


# API for the new Student module for them to read
class StudentAttendanceAPI(APIView):
    def get(self, request, student_id):
        cache_key = f"attendance:student:{student_id}"
        data = cache.get(cache_key)

        if data is None:
            logger.warning("CACHE MISS → DB QUERY - 2")
            records = (
                Attendance.objects
                .filter(student_id=student_id)
                .values("date", "present")
                .order_by("date")
            )
            data = list(records)
            cache.set(cache_key, data, 600)
        else:
            logger.warning("CACHE HIT - 2")

        # print("PID:", os.getpid())
        return Response(data)
