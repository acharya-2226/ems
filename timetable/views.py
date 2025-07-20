from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# from attendance.views import download_timetable
from .forms import TimetableForm, TimetableFilterForm
from .models import Timetable
from collections import defaultdict
import csv

@login_required
def view_timetable(request):
    timetables = Timetable.objects.all().order_by('day', 'time_slot__start_time')
    return render(request, 'timetable/view_timetable.html', {'timetables': timetables})


@login_required
def dashboard_timetable(request):
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

    return render(request, 'timetable/dashboard_timetable.html', {
        'filter_form': form,
        'grouped_timetables': dict(grouped),  # Send as a dict
    })

@login_required
def create_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_timetable')
    else:
        form = TimetableForm()

    return render(request, 'timetable/create_timetable.html', {'form': form})

@login_required
def edit_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('dashboard_timetable')
    else:
        form = TimetableForm(instance=timetable)

    return render(request, 'timetable/edit_timetable.html', {'form': form})

from django.shortcuts import get_object_or_404
@login_required
def delete_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        return redirect('dashboard_timetable')
    
    return render(request, 'timetable/delete_timetable.html', {'timetable': timetable})

from django.http import HttpResponse
def export_timetable(request):
    # 'request' is required by Django view signature
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="timetable.csv"'
    response['Content-Disposition'] = 'attachment; filename="timetable.csv"'

    writer = csv.writer(response)
    writer.writerow(['Day', 'Time Slot', 'Subject', 'Teacher', 'Room', 'Semester', 'Active'])

    for timetable in Timetable.objects.all():
        writer.writerow([timetable.day, timetable.time_slot, timetable.subject, timetable.teacher, timetable.room, timetable.semester, timetable.active])

    return response

@login_required
def download_timetable(request):
    # This function is not used in the current code, but can be implemented if needed
    return redirect('view_timetable')

@login_required
def show_all_urls(request):
    from django.urls import get_resolver
    resolver = get_resolver()
    urls = resolver.reverse_dict.keys()
    return render(request, 'timetable/show_all_urls.html', {'urls': urls})



