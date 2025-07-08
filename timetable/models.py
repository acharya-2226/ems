from django.db import models

class Timetable(models.Model):
    DAY_CHOICES = [
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]

    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    classroom = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.subject} ({self.day}) {self.start_time}-{self.end_time}"
