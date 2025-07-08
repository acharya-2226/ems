from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance_dashboard'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('view/teacher/', views.view_teacher_attendance, name='view_teacher'),
    path('view/student/', views.view_student_attendance, name='view_student'),
    path('view/admin/', views.view_admin_attendance, name='view_admin'),
    path('report', views.attendance_report, name='attendance_report'),
]
