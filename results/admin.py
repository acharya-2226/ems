from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'subject', 'marks_obtained', 'grade', 'published_date')
    list_filter = ('published_date', 'grade')
    search_fields = ('student_name', 'subject')
