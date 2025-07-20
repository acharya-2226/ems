from django.contrib import admin
from .models import Teacher, Subject, Room, TimeSlot, Timetable


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')  # ✅ 'name' exists in Room model


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')  # ✅ Only show actual fields
    ordering = ('start_time',)  # ✅ Optional, makes sense chronologically


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day', 'time_slot', 'subject', 'teacher', 'room', 'semester', 'active')
    list_filter = ('day', 'semester', 'active', 'room', 'teacher')
    search_fields = ('subject__name', 'teacher__name', 'room__name')
    ordering = ('day', 'time_slot')
