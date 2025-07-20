from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm


@login_required
def dashboard_assignments(request):
    """Dashboard for assignments with recent assignments."""
    assignments = Assignment.objects.all().order_by('-created_at')[:5]
    total_assignments = Assignment.objects.count()
    total_submissions = Submission.objects.count()
    
    context = {
        'assignments': assignments,
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
    }
    return render(request, 'assignments/dashboard_assignments.html', context)


@login_required
def upload_assignments(request):
    """Upload new assignments."""
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment uploaded successfully.")
            return redirect('assignments:dashboard_assignments')
    else:
        form = AssignmentForm()
    return render(request, 'assignments/upload_assignments.html', {'form': form})


@login_required
def view_assignments(request):
    """List all assignments."""
    assignments_list = Assignment.objects.all().order_by('-due_date')
    paginator = Paginator(assignments_list, 10)
    
    page_number = request.GET.get('page')
    assignments = paginator.get_page(page_number)
    
    return render(request, 'assignments/view_assignments.html', {'assignments': assignments})


@login_required
def submissions_assignments(request):
    """View all submissions."""
    submissions_list = Submission.objects.select_related('student', 'assignment').order_by('-submitted_at')
    paginator = Paginator(submissions_list, 10)

    page_number = request.GET.get('page')
    submissions = paginator.get_page(page_number)

    context = {
        'submissions': submissions,
    }
    return render(request, 'assignments/submissions_assignments.html', context)


@login_required
def report_assignments(request):
    """Generate assignment reports."""
    total_assignments = Assignment.objects.count()
    total_submissions = Submission.objects.count()
    graded_submissions = Submission.objects.exclude(grade__isnull=True).count()
    pending_submissions = Submission.objects.filter(grade__isnull=True).count()
    
    context = {
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'graded_submissions': graded_submissions,
        'pending_submissions': pending_submissions,
    }
    return render(request, 'assignments/report_assignments.html', context)


@login_required
def delete_assignments(request, pk):
    """Delete an assignment."""
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, "Assignment deleted successfully.")
        return redirect('assignments:view_assignments')
    return render(request, 'assignments/confirm_delete.html', {'assignment': assignment})


@method_decorator(login_required, name='dispatch')
class EditAssignmentView(UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/edit_assignments.html'
    success_url = reverse_lazy('assignments:dashboard_assignments')
    
    def form_valid(self, form):
        messages.success(self.request, "Assignment updated successfully.")
        return super().form_valid(form)