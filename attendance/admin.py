from django.contrib import admin
from .models import Subject, Student, AttendanceRecord


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'department']
    search_fields = ['user__username', 'roll_number', 'department']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'date', 'status']
    list_filter = ['status', 'date', 'subject']
    search_fields = ['student__user__username', 'subject__name']
    ordering = ['-date']
