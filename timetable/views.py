from django.shortcuts import render

def dashboard_timetable(request):
    return render(request, 'timetable/dashboard_timetable.html')

def create_timetable(request):
    return render(request, 'timetable/create_timetable.html')

def view_timetable(request):
    return render(request, 'timetable/view_timetable.html')

def download_timetable(request):
    return render(request, 'timetable/download_timetable.html')
