from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'subject', 'date')  # To avoid duplicates

    def __str__(self):
        return f"{self.student} - {self.subject.code} - {self.date} - {self.status}"
