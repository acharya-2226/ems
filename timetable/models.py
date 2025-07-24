from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Timetable(models.Model):
    MONDAY = 'Mon'
    TUESDAY = 'Tue'
    WEDNESDAY = 'Wed'
    THURSDAY = 'Thu'
    FRIDAY = 'Fri'

    DAYS_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
    ]
    # Fix imports to use core models
    time_slot = models.ForeignKey('core.TimeSlot', on_delete=models.CASCADE, related_name='timetables', null=True, blank=True)
    subject = models.ForeignKey('core.Subject', on_delete=models.CASCADE, related_name='timetables', null=True, blank=True)
    teacher = models.ForeignKey('core.Teacher', on_delete=models.CASCADE, related_name='timetables', null=True, blank=True)
    room = models.ForeignKey('core.Room', on_delete=models.CASCADE, related_name='timetables', null=True, blank=True)
    day = models.CharField(
        max_length=3,
        choices=DAYS_CHOICES,
        default=MONDAY
    )
    active = models.BooleanField(default=True)
    
    # Add proper validation
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    
    def clean(self):
        # Check for conflicts
        conflicts = Timetable.objects.filter(
            day=self.day,
            time_slot=self.time_slot,
            room=self.room,
            active=True
        ).exclude(id=self.id)
        
        if conflicts.exists():
            raise ValidationError('Room is already booked for this time slot')
        
        # Check teacher availability
        teacher_conflicts = Timetable.objects.filter(
            day=self.day,
            time_slot=self.time_slot,
            teacher=self.teacher,
            active=True
        ).exclude(id=self.id)
        
        if teacher_conflicts.exists():
            raise ValidationError('Teacher is already assigned for this time slot')