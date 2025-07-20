from django.db import models
from django.conf import settings


class Teacher(models.Model):    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Timetable(models.Model):
    DAYS_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=1)  # Default added here
    semester = models.IntegerField(default=1)  # Default added here
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('day', 'time_slot', 'room')

    def __str__(self):
        return f"{self.day} {self.time_slot} - {self.subject}"
