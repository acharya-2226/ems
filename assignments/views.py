from django.shortcuts import render
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404, redirect
from .models import Assignment 
from .forms import AssignmentForm


def dashboard_assignments(request):
    return render(request, 'assignments/dashboard_assignments.html')

def upload_assignments(request):
    return render(request, 'assignments/upload_assignments.html')

def view_submissions(request):
    return render(request, 'assignments/view_submissions.html')

def report_assignments(request):
    return render(request, 'assignments/report_assignments.html')

class EditAssignmentView(UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/edit_assignments.html'
    success_url = '/assignments/'
