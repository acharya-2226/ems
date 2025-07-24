from django.contrib import admin
from .models import Timetable


# Remove all core model registrations - they're handled in core/admin.py
# Only register models that belong to the timetable app

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day', 'time_slot', 'subject', 'teacher', 'room', 'semester', 'active')
    list_filter = ('day', 'semester', 'active', 'room', 'teacher')
    search_fields = ('subject__name', 'teacher__name', 'room__name')
    ordering = ('day', 'time_slot')
    list_editable = ('active',)  # Allow quick activation/deactivation
    
    # Group fields logically in the form
    fieldsets = (
        ('Schedule Details', {
            'fields': ('day', 'time_slot', 'semester')
        }),
        ('Academic Assignment', {
            'fields': ('subject', 'teacher', 'room')
        }),
        ('Status', {
            'fields': ('active',)
        }),
    )
    
    # Add some helpful methods
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'subject', 'teacher', 'room', 'time_slot'
        )
    
    def get_changelist_instance(self, request):
        # Expose days choices for use in the admin if needed
        self.days_choices = Timetable._meta.get_field('day').choices
        return super().get_changelist_instance(request)


# Add custom admin actions for timetable management
@admin.action(description='Activate selected timetable entries')
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.action(description='Deactivate selected timetable entries')
def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


# Add the actions to TimetableAdmin
TimetableAdmin.actions = [make_active, make_inactive]