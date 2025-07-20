from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'subject', 'marks_obtained', 'grade', 'created_at', 'published')
    list_filter = ('created_at', 'grade', 'published')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'subject__name')

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'
