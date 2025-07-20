from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.dashboard_assignments, name='dashboard_assignments'),
    path('upload/', views.upload_assignments, name='upload_assignments'),
    path('view/', views.view_assignments, name='view_assignments'),
    path('submissions/', views.submissions_assignments, name='submissions_assignments'),
    path('report/', views.report_assignments, name='report_assignments'),
    path('edit/<int:pk>/', views.EditAssignmentView.as_view(), name='edit_assignments'),
    path('delete/<int:pk>/', views.delete_assignments, name='delete_assignments'),
]
