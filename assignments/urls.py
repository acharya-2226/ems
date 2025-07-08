from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.dashboard_assignments, name='dashboard'),
    path('upload/', views.upload_assignments, name='upload_assignments'),
    path('submissions/', views.view_submissions, name='view_submissions'),
    path('report/', views.report_assignments, name='report_assignments'),
    path('submit/', views.report_assignments, name='submissions_assignments'),
]
