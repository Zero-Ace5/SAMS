from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    s_class = models.CharField(max_length=20)
    email = models.CharField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)

    class Meta:
        unique_together = ("student", "date")

    def __str__(self):
        return f"{self.student} ({self.date})"
