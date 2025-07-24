from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, timedelta
import csv

from .models import Student, AttendanceRecord
from .forms import BulkAttendanceForm, AttendanceReportForm, StudentAttendanceFilterForm
from core.models import Subject


@login_required
def attendance_dashboard(request):
    """Display the attendance dashboard with statistics."""
    context = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.filter(is_active=True).count(),
        'today_attendance_count': AttendanceRecord.objects.filter(
            date=timezone.now().date()
        ).count(),
    }
    
    # Add role-specific data
    if hasattr(request.user, 'attendance_student'):
        student = request.user.attendance_student
        context['student_percentage'] = student.get_attendance_percentage()
        context['student'] = student
    
    return render(request, 'attendance/dashboard.html', context)


@login_required
def mark_attendance(request):
    """Mark attendance for students with improved checkbox interface."""
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST, user=request.user)
        if form.is_valid():
            date = form.cleaned_data['date']
            subject = form.cleaned_data['subject']
            
            # Get attendance data from POST
            attendance_data = {}
            for key, value in request.POST.items():
                if key.startswith('attendance_'):
                    student_id = key.split('_')[1]
                    attendance_data[student_id] = value

            success_count = 0
            error_count = 0

            # Process each student in the subject
            students = subject.enrolled_students.filter(is_active=True)
            for student in students:
                try:
                    status = attendance_data.get(str(student.id), 'Absent')
                    
                    attendance_record, created = AttendanceRecord.objects.update_or_create(
                        student=student,
                        subject=subject,
                        date=date,
                        defaults={
                            'status': status,
                            'marked_by': request.user,
                        }
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Error marking attendance for {student}: {e}")

            if success_count > 0:
                messages.success(
                    request, 
                    f"Attendance marked successfully for {success_count} students."
                )
            if error_count > 0:
                messages.warning(
                    request, 
                    f"Failed to mark attendance for {error_count} students."
                )
                
            return redirect('attendance:attendance_dashboard')
    else:
        form = BulkAttendanceForm(initial={'date': timezone.now().date()}, user=request.user)

    # Get students based on selected subject (via AJAX)
    students = []
    selected_subject_id = request.GET.get('subject_id')
    if selected_subject_id:
        try:
            subject = Subject.objects.get(id=selected_subject_id, is_active=True)
            students = subject.enrolled_students.filter(is_active=True).order_by('roll_number')
            
            # Get existing attendance for the date if provided
            selected_date = request.GET.get('date')
            if selected_date:
                try:
                    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
                    existing_attendance = AttendanceRecord.objects.filter(
                        subject=subject,
                        date=date_obj
                    ).values('student_id', 'status')
                    
                    attendance_dict = {record['student_id']: record['status'] 
                                     for record in existing_attendance}
                    
                    # Add existing status to students
                    for student in students:
                        student.existing_status = attendance_dict.get(student.id, 'Present')
                        
                except ValueError:
                    pass
        except Subject.DoesNotExist:
            pass

    context = {
        'form': form,
        'students': students,
        'selected_subject_id': selected_subject_id,
    }
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
def get_students_by_subject(request):
    """AJAX endpoint to get students for a specific subject."""
    subject_id = request.GET.get('subject_id')
    date = request.GET.get('date')
    
    if not subject_id:
        return JsonResponse({'students': []})
    
    try:
        subject = Subject.objects.get(id=subject_id, is_active=True)
        students = subject.enrolled_students.filter(is_active=True).order_by('roll_number')
        
        students_data = []
        existing_attendance = {}
        
        # Get existing attendance if date is provided
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                attendance_records = AttendanceRecord.objects.filter(
                    subject=subject,
                    date=date_obj
                ).values('student_id', 'status')
                existing_attendance = {record['student_id']: record['status'] 
                                     for record in attendance_records}
            except ValueError:
                pass
        
        for student in students:
            students_data.append({
                'id': student.id,
                'name': student.full_name,
                'roll_number': student.roll_number,
                'existing_status': existing_attendance.get(student.id, 'Present')
            })
            
        return JsonResponse({'students': students_data})
    except Subject.DoesNotExist:
        return JsonResponse({'students': []})


@login_required
def view_student_attendance(request):
    """View attendance records for a student."""
    # Determine which student to show
    student = None
    if hasattr(request.user, 'attendance_student'):
        # Current user is a student
        student = request.user.attendance_student
    else:
        # Admin/Teacher viewing specific student
        student_id = request.GET.get('student_id')
        if student_id:
            student = get_object_or_404(Student, id=student_id, is_active=True)
    
    if not student:
        messages.error(request, "Student not found.")
        return redirect('attendance:attendance_dashboard')

    # Apply filters
    filter_form = StudentAttendanceFilterForm(request.GET, student=student)
    attendance_records = student.attendance_records.all()
    
    if filter_form.is_valid():
        subject = filter_form.cleaned_data.get('subject')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        
        if subject:
            attendance_records = attendance_records.filter(subject=subject)
        if start_date:
            attendance_records = attendance_records.filter(date__gte=start_date)
        if end_date:
            attendance_records = attendance_records.filter(date__lte=end_date)
    
    attendance_records = attendance_records.order_by('-date')
    
    # Pagination
    paginator = Paginator(attendance_records, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_records = attendance_records.count()
    present_count = attendance_records.filter(status='Present').count()
    attendance_percentage = round((present_count / total_records * 100), 2) if total_records > 0 else 0

    context = {
        'student': student,
        'attendance_records': page_obj,
        'filter_form': filter_form,
        'total_records': total_records,
        'present_count': present_count,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'attendance/view_attendance_student.html', context)


@login_required
def view_admin_attendance(request):
    """View all attendance records for admin."""
    # Apply filters
    filter_form = AttendanceReportForm(request.GET)
    attendance_records = AttendanceRecord.objects.all()
    
    if filter_form.is_valid():
        student = filter_form.cleaned_data.get('student')
        subject = filter_form.cleaned_data.get('subject')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        status = filter_form.cleaned_data.get('status')
        
        
        if student:
            attendance_records = attendance_records.filter(student=student)
        if subject:
            attendance_records = attendance_records.filter(subject=subject)
        if start_date:
            attendance_records = attendance_records.filter(date__gte=start_date)
        if end_date:
            attendance_records = attendance_records.filter(date__lte=end_date)
        if status:
            attendance_records = attendance_records.filter(status=status)
    
    attendance_records = attendance_records.select_related('student__user', 'subject').order_by('-date')
    
    # Pagination
    paginator = Paginator(attendance_records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'attendance_records': page_obj,
        'filter_form': filter_form,
        'today': timezone.now().date(),
        'total_records': attendance_records.count(),
    }
    return render(request, 'attendance/view_attendance_admin.html', context)


@login_required
def view_teacher_attendance(request):
    """View attendance records for a teacher's subjects."""
    # Get subjects taught by the teacher
    if hasattr(request.user, 'taught_subjects'):
        teacher_subjects = Subject.objects.filter(teacher=request.user, is_active=True)

    
    selected_subject_id = request.GET.get('subject_id')
    selected_subject = None
    attendance_records = AttendanceRecord.objects.none()
    
    if selected_subject_id:
        try:
            selected_subject = teacher_subjects.get(id=selected_subject_id)
            attendance_records = AttendanceRecord.objects.filter(
                subject=selected_subject
            ).select_related('student__user').order_by('-date', 'student__roll_number')
        except Subject.DoesNotExist:
            messages.error(request, "Subject not found or you don't have permission to view it.")

    # Pagination
    paginator = Paginator(attendance_records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'teacher_subjects': teacher_subjects,
        'selected_subject': selected_subject,
        'attendance_records': page_obj,
    }
    return render(request, 'attendance/view_attendance_teacher.html', context)


@login_required
def attendance_report(request):
    """Generate comprehensive attendance report."""
    filter_form = AttendanceReportForm(request.GET)
    attendance_records = AttendanceRecord.objects.none()
    statistics = {}
    
    if filter_form.is_valid():
        attendance_records = AttendanceRecord.objects.all()
        
        student = filter_form.cleaned_data.get('student')
        subject = filter_form.cleaned_data.get('subject')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        status = filter_form.cleaned_data.get('status')
        
        if student:
            attendance_records = attendance_records.filter(student=student)
        if subject:
            attendance_records = attendance_records.filter(subject=subject)
        if start_date:
            attendance_records = attendance_records.filter(date__gte=start_date)
        if end_date:
            attendance_records = attendance_records.filter(date__lte=end_date)
        if status:
            attendance_records = attendance_records.filter(status=status)
        
        attendance_records = attendance_records.select_related('student__user', 'subject').order_by('-date')
        
        # Calculate statistics
        total_records = attendance_records.count()
        if total_records > 0:
            status_counts = attendance_records.values('status').annotate(count=Count('status'))
            statistics = {item['status']: item['count'] for item in status_counts}
            statistics['total'] = total_records
            
            # Calculate percentages
            for status_key in statistics:
                if status_key != 'total':
                    statistics[f'{status_key.lower()}_percentage'] = round(
                        (statistics[status_key] / total_records * 100), 2
                    )

    # Pagination
    paginator = Paginator(attendance_records, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter_form': filter_form,
        'attendance_records': page_obj,
        'statistics': statistics,
    }
    return render(request, 'attendance/attendance_report.html', context)


@login_required
def export_attendance_csv(request):
    """Export attendance records to CSV."""
    # Apply same filters as the report
    filter_form = AttendanceReportForm(request.GET)
    attendance_records = AttendanceRecord.objects.all()
    
    if filter_form.is_valid():
        student = filter_form.cleaned_data.get('student')
        subject = filter_form.cleaned_data.get('subject')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        status = filter_form.cleaned_data.get('status')
        
        if student:
            attendance_records = attendance_records.filter(student=student)
        if subject:
            attendance_records = attendance_records.filter(subject=subject)
        if start_date:
            attendance_records = attendance_records.filter(date__gte=start_date)
        if end_date:
            attendance_records = attendance_records.filter(date__lte=end_date)
        if status:
            attendance_records = attendance_records.filter(status=status)
    
    attendance_records = attendance_records.select_related('student__user', 'subject').order_by('-date')
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_report_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Student Name', 'Roll Number', 'Subject', 'Status', 'Marked By'])
    
    for record in attendance_records:
        writer.writerow([
            record.date.strftime('%Y-%m-%d'),
            record.student.full_name,
            record.student.roll_number,
            f"{record.subject.name} ({record.subject.code})",
            record.status,
            record.marked_by.get_full_name() if record.marked_by else 'N/A'
        ])
    
    return response

def get_attendance_percentage(student, subject=None):
    """Calculate attendance percentage for a student in a specific subject."""
    if subject:
        records = AttendanceRecord.objects.filter(student=student, subject=subject)
    else:
        records = AttendanceRecord.objects.filter(student=student)
    
    total_classes = records.count()
    present_count = records.filter(status='Present').count()
    
    if total_classes == 0:
        return 0.0
    
    return round((present_count / total_classes) * 100, 2)