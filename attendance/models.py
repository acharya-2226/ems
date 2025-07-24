from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from core.models import Student

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records', null=True, blank=True)
    subject = models.ForeignKey('core.Subject', on_delete=models.CASCADE, related_name='attendance_records', null=True, blank=True)
    date = models.DateField(null=True, blank=True, default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    remarks = models.TextField(blank=True, null=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendances'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def clean(self):
        from datetime import date, timedelta
        if self.date is not None:
            if self.date > date.today():
                raise ValidationError("Cannot mark attendance for future dates")
            if self.date < date.today() - timedelta(days=30):
                raise ValidationError("Cannot mark attendance older than 30 days")

    class Meta:
        unique_together = ('student', 'subject', 'date')
        ordering = ['-date', 'student__roll_number']
        indexes = [
            models.Index(fields=['date', 'subject']),
            models.Index(fields=['student', 'date']),
        ]

    def __str__(self):
        return f"{self.student} - {self.subject.code} - {self.date} - {self.status}"
