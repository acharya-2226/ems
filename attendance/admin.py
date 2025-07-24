from django.contrib import admin
from .models import Student, AttendanceRecord

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'department', 'is_active']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'roll_number', 'department']
    list_filter = ['is_active', 'department']
    filter_horizontal = ['subjects']

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date', 'subject']
    search_fields = ['student__user__username', 'student__roll_number', 'subject__name']
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']