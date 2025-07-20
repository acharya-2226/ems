from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Student, AttendanceRecord, Subject
from .forms import BulkAttendanceForm


@login_required
def mark_attendance(request):
    """Mark attendance for students."""
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            subject = form.cleaned_data['subject']

            # Process attendance statuses for each student
            for key, value in request.POST.items():
                if key.startswith('student_'):
                    student_id = key.split('_')[1]
                    status = value
                    student = get_object_or_404(Student, id=student_id)

                    AttendanceRecord.objects.update_or_create(
                        student=student,
                        subject=subject,
                        date=date,
                        defaults={'status': status}
                    )
            messages.success(request, "Attendance marked successfully.")
            return redirect('attendance:attendance_dashboard')
    else:
        form = BulkAttendanceForm(initial={'date': timezone.now().date()})

    students = Student.objects.all()
    context = {
        'form': form,
        'students': students,
    }
    return render(request, 'attendance/mark_attendance.html', context)

@login_required
def attendance_dashboard(request):
    """Display the attendance dashboard."""
    return render(request, 'attendance/dashboard.html')

@login_required
def view_student_attendance(request):
    """View attendance records for a specific student."""
    student_id = request.GET.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    attendance_records = AttendanceRecord.objects.filter(student=student).order_by('-date')

    paginator = Paginator(attendance_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'student': student,
        'attendance_records': page_obj
    }
    return render(request, 'attendance/view_student_attendance.html', context)

@login_required
def attendance_report(request):
    """Generate attendance report."""
    return render(request, 'attendance/attendance_report.html')

@login_required
def attendance_dashboard(request):
    """Display the attendance dashboard."""
    return render(request, 'attendance/dashboard.html')

@login_required
def view_admin_attendance(request):
    """View all attendance records for admin."""
    attendance_records = AttendanceRecord.objects.all().order_by('-date')

    paginator = Paginator(attendance_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'attendance_records': page_obj
    }
    return render(request, 'attendance/view_admin_attendance.html', context)

@login_required
def view_teacher_attendance(request):
    """View attendance records for a specific teacher."""
    subject_id = request.GET.get('subject_id')
    subject = get_object_or_404(Subject, id=subject_id)
    attendance_records = AttendanceRecord.objects.filter(subject=subject).order_by('-date')

    paginator = Paginator(attendance_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'subject': subject,
        'attendance_records': page_obj
    }
    return render(request, 'attendance/view_attendance_teacher.html', context)

