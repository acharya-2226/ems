from django.db import models
from django.conf import settings


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/')
    due_date = models.DateField(null=True, blank=True)  # example field you might have added
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('graded', 'Graded'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)  # Grade field added

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
