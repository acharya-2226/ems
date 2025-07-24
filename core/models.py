from django.db import models

from django.core.exceptions import ValidationError
import re
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils import timezone


ROOM_TYPE_CHOICES = [
    ('Lecture Hall', 'Lecture Hall'),
    ('Laboratory', 'Laboratory'),
    ('Seminar Room', 'Seminar Room'),
    ('Conference Room', 'Conference Room'),
    ('Other', 'Other')
]

class Subject(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects'
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    credits = models.PositiveIntegerField(default=3, null=True, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True, related_name='subjects')

    def clean(self):
        if self.code and not re.match(r'^[A-Z]{2,4}[0-9]{3,4}$', self.code):
            raise ValidationError('Subject code must be in format like CS101')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    building = models.CharField(max_length=100, null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, null=True, blank=True)
    equipment = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def clean(self):
        if self.capacity and self.capacity > 500:  # Reasonable max capacity
            raise ValidationError('Room capacity cannot exceed 500')

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Teacher(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE,
            related_name='teacher_profile',
            default=None,
            null=True
        )
    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers',
        
    )
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    head = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_head'
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.code and not re.match(r'^[A-Z]{2,4}$', self.code):
            raise ValidationError('Department code must be in format like CS')
        if self.head and hasattr(self.head, 'department') and self.head.department != self:
            raise ValidationError('Department head must belong to the department')

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='attendance_student_profile',
        default=None,
        null=True,
    )
    department = models.OneToOneField(
        'core.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_student_profile'
    )
    roll_number = models.CharField(
        max_length=20, 
        unique=True, 
        blank=True, 
        null=True,
        help_text="Unique roll number for the student"
    )
    subjects = models.ManyToManyField('core.Subject', related_name='enrolled_students')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def clean(self):
        if self.roll_number is not None and not re.match(r'^[A-Za-z0-9]+$', self.roll_number):
            raise ValidationError("Roll number can only contain alphanumeric characters.")

    class Meta:
        ordering = ['roll_number']

    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name()} ({self.roll_number})"
        return f"Student ({self.roll_number})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username
    @property
    def email(self):
        return self.user.email if self.user else None
    @property
    def username(self):
        return self.user.username if self.user else None
    @property
    def profile_picture(self):
        return self.user.profile_picture if self.user and hasattr(self.user, 'profile_picture') else None
    @property
    def department_name(self):
        return self.department.name if self.department else "No Department"
    
    @property   
    def subjects_list(self):
        return [subject.name for subject in self.subjects.all()] if self.subjects.exists() else ["No Subjects Enrolled"]            