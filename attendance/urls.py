from django.urls import path
from . import views

app_name = 'attendance'  # For namespacing URLs

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance_dashboard'),  # dashboard view (you can add it)
    path('mark/', views.mark_attendance, name='mark_attendance'),       # your mark attendance page
    path('view_student/', views.view_student_attendance, name='view_student_attendance'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('view_admin/', views.view_admin_attendance, name='view_admin'),
    path('view_teacher/', views.view_teacher_attendance, name='view_teacher'),
]
