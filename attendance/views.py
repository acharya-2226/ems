from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Student, AttendanceRecord
from django.utils.timezone import now


def attendance_dashboard(request):
    return render(request, 'attendance/dashboard_attendance.html')

def mark_attendance(request):
    return render(request, 'attendance/mark_attendance.html')

def view_teacher_attendance(request):
    return render(request, 'attendance/view_attendance_teacher.html')

def view_student_attendance(request):
    return render(request, 'attendance/view_attendance_student.html')

def view_admin_attendance(request):
    return render(request, 'attendance/view_attendance_admin.html')

def attendance_report(request):
    return render(request, 'attendance/report_attendance.html')


