from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import TimetableForm, TimetableFilterForm
from .models import Timetable
from collections import defaultdict
import csv


@login_required
def view_timetable(request):
    try:
        timetables = Timetable.objects.all().order_by('day', 'time_slot__start_time')
    except:
        timetables = []
    return render(request, 'timetable/view_timetable.html', {'timetables': timetables})

@login_required
def dashboard_timetable(request):
    try:
        form = TimetableFilterForm(request.GET or None)
        timetables = Timetable.objects.all().order_by('day', 'time_slot__start_time')

        if form.is_valid():
            day = form.cleaned_data.get('day')
            semester = form.cleaned_data.get('semester')
            teacher = form.cleaned_data.get('teacher')

            if day:
                timetables = timetables.filter(day=day)
            if semester:
                timetables = timetables.filter(semester=semester)
            if teacher:
                timetables = timetables.filter(teacher=teacher)

        grouped = defaultdict(list)
        for timetable in timetables:
            grouped[timetable.day].append(timetable)
            
    except:
        form = TimetableFilterForm()
        grouped = {}

    return render(request, 'timetable/dashboard_timetable.html', {
        'filter_form': form,
        'grouped_timetables': dict(grouped),
    })

@login_required
def create_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('timetable:dashboard_timetable')
            except:
                form.add_error(None, "Error creating timetable. Please try again.")
        else:
            form.add_error(None, "Please correct the errors below.")
    else:
        form = TimetableForm()

    return render(request, 'timetable/create_timetable.html', {'form': form})

@login_required
def edit_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            try:
                form.save()
                return redirect('timetable:dashboard_timetable')
            except:
                form.add_error(None, "Error updating timetable. Please try again.")
        else:
            form.add_error(None, "Please correct the errors below.")
    else:
        form = TimetableForm(instance=timetable)

    return render(request, 'timetable/edit_timetable.html', {'form': form, 'timetable': timetable})

@login_required
def delete_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        try:
            timetable.delete()
            return redirect('timetable:dashboard_timetable')
        except:
            return render(request, 'timetable/delete_timetable.html', {
                'timetable': timetable,
                'error': 'Error deleting timetable. Please try again.'
            })
    
    return render(request, 'timetable/delete_timetable.html', {'timetable': timetable})

@login_required
@login_required
def export_timetable(request):
    try:
        # Apply same filters as download page
        timetables = Timetable.objects.all()
        
        form = TimetableFilterForm(request.GET or None)
        if form.is_valid():
            day = form.cleaned_data.get('day')
            semester = form.cleaned_data.get('semester')
            teacher = form.cleaned_data.get('teacher')
            subject = form.cleaned_data.get('subject')

            if day:
                timetables = timetables.filter(day=day)
            if semester:
                timetables = timetables.filter(semester=semester)
            if teacher:
                timetables = timetables.filter(teacher=teacher)
            if subject:
                timetables = timetables.filter(subject=subject)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="timetable.csv"'

        writer = csv.writer(response)
        writer.writerow(['Day', 'Time Slot', 'Subject', 'Teacher', 'Room', 'Semester', 'Active'])

        for timetable in timetables:
            writer.writerow([
                timetable.day, 
                str(timetable.time_slot), 
                str(timetable.subject), 
                str(timetable.teacher), 
                timetable.room, 
                timetable.semester, 
                timetable.active
            ])

        return response
    except:
        return redirect('timetable:dashboard_timetable')

@login_required
@login_required
def download_timetable(request):
    # Handle download format requests
    download_format = request.GET.get('format', '')
    
    if download_format == 'csv':
        return export_timetable(request)
    elif download_format == 'json':
        return export_timetable_json(request)
    
    # Otherwise show the download page
    try:
        form = TimetableFilterForm(request.GET or None)
        timetables = Timetable.objects.all()
        
        if form.is_valid():
            day = form.cleaned_data.get('day')
            semester = form.cleaned_data.get('semester')
            teacher = form.cleaned_data.get('teacher')
            subject = form.cleaned_data.get('subject')

            if day:
                timetables = timetables.filter(day=day)
            if semester:
                timetables = timetables.filter(semester=semester)
            if teacher:
                timetables = timetables.filter(teacher=teacher)
            if subject:
                timetables = timetables.filter(subject=subject)
        
        total_count = timetables.count()
        
    except:
        form = TimetableFilterForm()
        total_count = 0
    
    context = {
        'filter_form': form,
        'total_count': total_count,
    }
    return render(request, 'timetable/download_timetable.html', context)

# Add this new function for JSON export
@login_required
def export_timetable_json(request):
    try:
        from django.http import JsonResponse
        
        timetables = Timetable.objects.all()
        
        # Apply same filters as download page
        form = TimetableFilterForm(request.GET or None)
        if form.is_valid():
            day = form.cleaned_data.get('day')
            semester = form.cleaned_data.get('semester')
            teacher = form.cleaned_data.get('teacher')
            subject = form.cleaned_data.get('subject')

            if day:
                timetables = timetables.filter(day=day)
            if semester:
                timetables = timetables.filter(semester=semester)
            if teacher:
                timetables = timetables.filter(teacher=teacher)
            if subject:
                timetables = timetables.filter(subject=subject)
        
        data = []
        for timetable in timetables:
            data.append({
                'day': timetable.day,
                'time_slot': str(timetable.time_slot),
                'subject': str(timetable.subject),
                'teacher': str(timetable.teacher),
                'room': timetable.room,
                'semester': timetable.semester,
                'active': timetable.active,
            })
        
        response = JsonResponse({'timetables': data})
        response['Content-Disposition'] = 'attachment; filename="timetable.json"'
        return response
        
    except:
        return redirect('timetable:dashboard_timetable')