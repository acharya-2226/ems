from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .admin_mixins import ExportImportAdminMixin  # ⬅️ Custom mixin

@admin.register(CustomUser)
class CustomUserAdmin(ExportImportAdminMixin,UserAdmin):  # ⬅️ Mixin added
    change_list_template = "admin/accounts/customuser/change_list_export_import.html"  # ⬅️ Override default changelist template
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'role', 'is_active', 'is_staff', 'created_at'
    ]
    list_filter = [
        'role', 'is_staff', 'is_superuser', 'is_active',
        'is_email_verified', 'created_at'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'roll_number']
    ordering = ['-created_at']

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('role', 'roll_number', 'microsoft_id', 'is_email_verified')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'role', 'roll_number', 'password1', 'password2',
            ),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    actions = ['activate_users', 'deactivate_users', 'mark_email_verified']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) were successfully activated.')
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"

    def mark_email_verified(self, request, queryset):
        updated = queryset.update(is_email_verified=True)
        self.message_user(request, f'{updated} user(s) were marked as email verified.')
    mark_email_verified.short_description = "Mark email as verified"
