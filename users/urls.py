from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.dashboard_users, name='dashboard'),
    path('view/', views.view_users, name='view_users'),
    path('add/', views.add_user, name='add_user'),
    # path('edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('roles/', views.roles_permissions, name='roles_permissions'),

]
