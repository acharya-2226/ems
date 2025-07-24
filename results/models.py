from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone


class Result(models.Model):
    student = models.ForeignKey('core.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('core.Subject', on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    marks_obtained = models.FloatField(validators=[MinValueValidator(0)], default=0)
    total_marks = models.FloatField(validators=[MinValueValidator(1)], default=100)

    grade = models.CharField(max_length=2, blank=True, default='')  # e.g. 'A+', 'B', etc.

    semester = models.PositiveSmallIntegerField(default=1)
    year = models.PositiveSmallIntegerField(default=timezone.now().year)

    published = models.BooleanField(default=False)

    def clean(self):
        if self.marks_obtained > self.total_marks:
            raise ValidationError('Marks obtained cannot exceed total marks')

    def save(self, *args, **kwargs):
        if self.marks_obtained is not None and self.total_marks:
            percentage = (self.marks_obtained / self.total_marks) * 100
            self.grade = self.calculate_grade(percentage)
        # Update updated_at on each save
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def calculate_grade(self, percentage):
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C+'
        elif percentage >= 40:
            return 'C'
        elif percentage >= 30:
            return 'D'
        else:
            return 'F'

    class Meta:
        unique_together = ('student', 'subject', 'semester', 'year')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"

    @property
    def percentage(self):
        if self.marks_obtained is not None and self.total_marks:
            return round((self.marks_obtained / self.total_marks) * 100, 2)
        return None
