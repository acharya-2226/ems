from django.contrib import admin
from django.utils.html import format_html
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'due_date', 'submission_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'due_date', 'created_by']
    search_fields = ['title', 'description', 'created_by__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'file', 'created_by')
        }),
        ('Scheduling', {
            'fields': ('due_date', 'max_score', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def submission_count(self, obj):
        count = obj.submissions.count()
        return format_html(
            '<span class="badge badge-primary">{}</span>',
            count
        )
    submission_count.short_description = 'Submissions'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'status', 'grade', 'score', 'is_late', 'submitted_at']
    list_filter = ['status', 'grade', 'submitted_at', 'graded_at']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'assignment__title']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at', 'is_late']
    
    def is_late(self, obj):
        return obj.is_late
    is_late.boolean = True
    is_late.short_description = 'Late Submission'