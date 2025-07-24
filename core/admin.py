from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Subject, Room, TimeSlot, Teacher, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher_count', 'subject_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'code')

    readonly_fields = ('created_at', 'teacher_count', 'subject_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code')
        }),
        ('Statistics', {
            'fields': ('teacher_count', 'subject_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('head').annotate(
            teachers_count=Count('teachers', distinct=True),
            subjects_count=Count('subjects', distinct=True)
        )
    
    def teacher_count(self, obj):
        return obj.teachers_count
    teacher_count.short_description = 'Teachers'
    teacher_count.admin_order_field = 'teachers_count'
    
    def subject_count(self, obj):
        return obj.subjects_count
    subject_count.short_description = 'Subjects'
    subject_count.admin_order_field = 'subjects_count'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department',  'is_active', 'hire_date', 'user')
    list_filter = ('is_active', 'department', 'hire_date')
    search_fields = ('name', 'email')
    date_hierarchy = 'hire_date'
    list_select_related = ('department', 'user')

    list_editable = ('is_active',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'user')
        }),
        ('Employment Details', {
            'fields': ('department', 'hire_date', 'is_active')
        }),
        ('System Information', {
            'fields': (),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department').annotate(
            subjects_count=Count('subjects')
        )
    
    def subject_count(self, obj):
        count = obj.subjects_count
        if count > 0:
            return format_html(
                '<a href="/admin/core/subject/?teacher__id__exact={}">{}</a>',
                obj.id, count
            )
        return count
    subject_count.short_description = 'Subjects'
    subject_count.admin_order_field = 'subjects_count'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher', 'department', 'credits', 'semester', 'is_active')
    list_filter = ('is_active', 'department', 'semester', 'credits')
    search_fields = ('name', 'code', 'teacher__name')
    
    
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Academic Details', {
            'fields': ('department', 'teacher', 'credits', 'semester')
        }),
        
        ('Status', {
            'fields': ('is_active', 'created_at'),
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher', 'department')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            # Log subject changes
            self.message_user(request, f"Subject {obj.code} updated successfully.")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'floor', 'capacity', 'room_type', 'is_active')
    list_filter = ('building', 'room_type', 'is_active')
    search_fields = ('name', 'building')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'building', 'floor')
        }),
        ('Specifications', {
            'fields': ('capacity', 'room_type', 'equipment')
        }),
       
    )

    

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'duration_display', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    ordering = ('start_time',)
    
    fieldsets = (
        ('Time Information', {
            'fields': ('name', 'start_time', 'end_time')
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )

    def duration_display(self, obj):
        today = datetime.today().date()
        start = datetime.combine(today, obj.start_time)
        end = datetime.combine(today, obj.end_time)
        duration = end - start
        return f"{int(duration.total_seconds() // 60)} min"
    duration_display.short_description = 'Duration'
    
from datetime import datetime, timedelta

   




# Custom admin site configuration
admin.site.site_header = "EMS Administration"
admin.site.site_title = "EMS Admin Portal"
admin.site.index_title = "Welcome to EMS Administration"


# Register any additional custom actions
@admin.action(description='Activate selected items')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Deactivate selected items')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


# Add actions to applicable admin classes
TeacherAdmin.actions = [make_active, make_inactive]
SubjectAdmin.actions = [make_active, make_inactive]
RoomAdmin.actions = [make_active, make_inactive]
TimeSlotAdmin.actions = [make_active, make_inactive]