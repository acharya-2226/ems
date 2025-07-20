from django.db import models
from django.conf import settings


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    credits = models.IntegerField(default=3, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results_student')
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


class Result(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (90-100)'),
        ('A', 'A (80-89)'),
        ('B+', 'B+ (70-79)'),
        ('B', 'B (60-69)'),
        ('C+', 'C+ (50-59)'),
        ('C', 'C (40-49)'),
        ('D', 'D (30-39)'),
        ('F', 'F (0-29)'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    marks_obtained = models.FloatField(blank=True, null=True)
    total_marks = models.FloatField(default=100, blank=True, null=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    published = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'subject', 'semester', 'year')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"

    @property
    def percentage(self):
        if self.marks_obtained is not None and self.total_marks:
            return round((self.marks_obtained / self.total_marks) * 100, 2)
        return None