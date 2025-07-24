from django.urls import path
from . import views


app_name = 'attendance'

urlpatterns = [
    # Dashboard
    path('', views.attendance_dashboard, name='dashboard'),
    
    # Attendance marking
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('api/students-by-subject/', views.get_students_by_subject, name='get_students_by_subject'),
    
    # Viewing attendance
    path('view/student/', views.view_student_attendance, name='view_student_attendance'),
    path('view/admin/', views.view_admin_attendance, name='view_admin'),
    path('view/teacher/', views.view_teacher_attendance, name='view_teacher'),
    
    # Reports
    path('report/', views.attendance_report, name='attendance_report'),
    path('export/csv/', views.export_attendance_csv, name='export_csv'),
]