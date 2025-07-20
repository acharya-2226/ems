from django.db import models
from django.conf import settings


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_student')
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        # Use user's full name properly
        return f"{self.user.get_full_name()} ({self.roll_number})"
    
    @property
    def full_name(self):
        return self.user.get_full_name()


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
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student} - {self.subject.code} - {self.date} - {self.status}"
