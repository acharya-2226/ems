from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils import timezone

class Assignment(models.Model):
    title = models.CharField(max_length=255, default='', help_text="Title of the assignment")
    description = models.TextField(default='', help_text="Detailed description of the assignment")
    file = models.FileField(
        upload_to='assignments/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text="Allowed formats: PDF, DOC, DOCX",
        blank=True,
        null=True,
        default=''
    )
    due_date = models.DateTimeField(null=True, blank=True)  # Changed to DateTime
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_assignments', null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    max_score = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['due_date']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('assignments:edit_assignments', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        if self.due_date:
            return timezone.now() > self.due_date
        return False
    
    @property
    def submission_count(self):
        return self.submissions.count()

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
    ]
    
    GRADE_CHOICES = [
        ('A+', 'A+ (97-100)'),
        ('A', 'A (93-96)'),
        ('A-', 'A- (90-92)'),
        ('B+', 'B+ (87-89)'),
        ('B', 'B (83-86)'),
        ('B-', 'B- (80-82)'),
        ('C+', 'C+ (77-79)'),
        ('C', 'C (73-76)'),
        ('C-', 'C- (70-72)'),
        ('D', 'D (60-69)'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True, default=None)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, default=None)
    submitted_file = models.FileField(
        upload_to='submissions/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])],
        blank=True,
        null=True,
        default=''
    )
    upload_to='submissions/',
    validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])]
    
    submitted_at = models.DateTimeField(default=timezone.now)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True, null=True)
    score = models.PositiveIntegerField(null=True, blank=True, help_text="Score out of max score")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    feedback = models.TextField(blank=True, help_text="Teacher's feedback")
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='graded_submissions'
    )

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['submitted_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
    
    @property
    def is_late(self):
        if self.assignment.due_date:
            return self.submitted_at > self.assignment.due_date
        return False
    
    def save(self, *args, **kwargs):
        # Auto-set status based on submission timing
        if self.is_late:
            self.status = 'late'
        super().save(*args, **kwargs)