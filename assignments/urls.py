from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.dashboard_assignments, name='dashboard_assignments'),
    path('upload/', views.upload_assignments, name='upload_assignments'),
    path('view/', views.view_assignments, name='view_assignments'),
    path('detail/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('submissions/', views.submissions_assignments, name='submissions_assignments'),
    path('grade/<int:pk>/', views.grade_submission, name='grade_submission'),
    path('report/', views.report_assignments, name='report_assignments'),
    path('edit/<int:pk>/', views.EditAssignmentView.as_view(), name='edit_assignments'),
    path('delete/<int:pk>/', views.delete_assignments, name='delete_assignments'),
    path('download/<int:pk>/', views.download_submission_file, name='download_submission'),
    path('api/assignments/', views.api_assignments, name='api_assignments'),
    path('api/submissions/', views.api_submissions, name='api_submissions'),
    path('api/submission/<int:pk>/', views.api_submission_detail, name='api_submission_detail'),
    path('api/create-submission/', views.api_create_submission, name='api_create_submission'),
]