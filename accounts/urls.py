from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('microsoft-signup/', views.microsoft_signup, name='microsoft_signup'),
    path('microsoft-callback/', views.microsoft_callback, name='microsoft_callback'),

    # Dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/users/', views.dashboard_users, name='dashboard_users'),

    # Admin user management
    path('dashboard/users/add/', views.add_user, name='add_user'),
    path('dashboard/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('dashboard/users/<int:user_id>/view/', views.view_user, name='view_user'),
    path('dashboard/users/<int:user_id>/role/', views.user_role, name='user_role'),
    path('dashboard/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('dashboard/users/roles-permissions/', views.roles_permissions, name='roles_permissions'),


    # Profile and settings
    path('profile/', views.profile, name='profile'),
    path('email/', views.email_settings, name='email_settings'),
    path('settings/', views.account_settings, name='settings'),

    # Import/Export
    path('customuser/download-format/', views.customuser_download_format, name='accounts_customuser_download_format'),
    path('customuser/import-xls/', views.customuser_import_xls, name='accounts_customuser_import_xls'),
]
