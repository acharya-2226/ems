# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser
# from .forms import CustomUserCreationForm, CustomUserChangeForm

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ('username', 'email', 'role', 'is_staff')
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('role', 'profile_picture')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('role', 'profile_picture')}),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)
