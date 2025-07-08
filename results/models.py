from django.db import models

class Result(models.Model):
    student_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()
    grade = models.CharField(max_length=5)
    published_date = models.DateField()

    def __str__(self):
        return f"{self.student_name} - {self.subject}"
