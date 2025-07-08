from django.contrib import admin
from .models import Timetable

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'subject', 'teacher', 'classroom')
    list_filter = ('day', 'teacher', 'classroom')
    search_fields = ('subject', 'teacher')
