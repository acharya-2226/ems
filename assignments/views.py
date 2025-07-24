from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q, Avg
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm, GradeSubmissionForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model



@login_required
def dashboard_assignments(request):
    """Enhanced dashboard with better analytics."""
    recent_assignments = Assignment.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Analytics
    total_assignments = Assignment.objects.filter(is_active=True).count()
    total_submissions = Submission.objects.count()
    pending_submissions = Submission.objects.filter(status='pending').count()
    overdue_assignments = Assignment.objects.filter(
        due_date__lt=timezone.now(),
        is_active=True
    ).count()
    
    context = {
        'recent_assignments': recent_assignments,
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'pending_submissions': pending_submissions,
        'overdue_assignments': overdue_assignments,
    }
    return render(request, 'assignments/dashboard_assignments.html', context)

@login_required
def upload_assignments(request):
    """Enhanced upload with better error handling."""
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, f"Assignment '{assignment.title}' uploaded successfully.")
            return redirect('assignments:dashboard_assignments')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AssignmentForm()
    return render(request, 'assignments/upload_assignments.html', {'form': form})

@login_required
def view_assignments(request):
    """Enhanced view with search and filtering."""
    assignments_list = Assignment.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        assignments_list = assignments_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter functionality
    status_filter = request.GET.get('status', '')
    if status_filter == 'overdue':
        assignments_list = assignments_list.filter(due_date__lt=timezone.now())
    elif status_filter == 'active':
        assignments_list = assignments_list.filter(due_date__gte=timezone.now())
    
    assignments_list = assignments_list.order_by('-due_date')
    paginator = Paginator(assignments_list, 10)
    
    page_number = request.GET.get('page')
    assignments = paginator.get_page(page_number)
    
    context = {
        'assignments': assignments,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'assignments/view_assignments.html', context)

@login_required
def report_assignments(request):
    """Enhanced report with real data."""
    # Get assignment statistics
    assignments_stats = Assignment.objects.annotate(
        submission_count=Count('submissions'),
        avg_score=Avg('submissions__score')
    ).filter(is_active=True)[:10]
    
    # Grade distribution
    grade_distribution = Submission.objects.exclude(grade__isnull=True).values('grade').annotate(count=Count('grade'))
    
    # Status distribution
    status_distribution = Submission.objects.values('status').annotate(count=Count('status'))
    
    context = {
        'assignments_stats': assignments_stats,
        'grade_distribution': list(grade_distribution),
        'status_distribution': list(status_distribution),
        'total_assignments': Assignment.objects.filter(is_active=True).count(),
        'total_submissions': Submission.objects.count(),
        'graded_submissions': Submission.objects.exclude(grade__isnull=True).count(),
        'pending_submissions': Submission.objects.filter(status='pending').count(),
    }
    return render(request, 'assignments/report_assignments.html', context)

# Add new views for better functionality
@login_required
def assignment_detail(request, pk):
    """View assignment details with submissions."""
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = assignment.submissions.select_related('student').order_by('-submitted_at')
    
    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'assignments/assignment_detail.html', context)

@login_required
def grade_submission(request, pk):
    """Grade a specific submission."""
    submission = get_object_or_404(Submission, pk=pk)
    
    # Check if user can grade (teacher/staff)
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to grade submissions.")
    
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.status = 'graded'
            submission.graded_by = request.user
            submission.graded_at = timezone.now()
            submission.save()
            messages.success(request, f"Grade submitted for {submission.student.username}")
            return redirect('assignments:submissions_assignments')
    else:
        form = GradeSubmissionForm(instance=submission)
    
    context = {
        'form': form,
        'submission': submission,
    }
    return render(request, 'assignments/grade_submission.html', context)

@login_required
def submissions_assignments(request):
    """View all submissions with filtering and sorting."""
    submissions = Submission.objects.select_related('assignment', 'student').order_by('-submitted_at')
    
    # Filter by assignment
    assignment_filter = request.GET.get('assignment', '')
    if assignment_filter:
        submissions = submissions.filter(assignment__id=assignment_filter)
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        submissions = submissions.filter(status=status_filter)
    
    paginator = Paginator(submissions, 10)
    page_number = request.GET.get('page')
    submissions_page = paginator.get_page(page_number)
    
    context = {
        'submissions': submissions_page,
        'assignments': Assignment.objects.all(),
        'assignment_filter': assignment_filter,
        'status_filter': status_filter,
    }
    return render(request, 'assignments/submissions_assignments.html', context)


@login_required
def delete_assignments(request, pk):
    """Delete an assignment."""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, f"Assignment '{assignment.title}' deleted successfully.")
        return redirect('assignments:dashboard_assignments')
    
    return render(request, 'assignments/delete_assignment.html', {'assignment': assignment})

@method_decorator(login_required, name='dispatch')
class EditAssignmentView(LoginRequiredMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/edit_assignment.html'
    success_url = reverse_lazy('assignments:dashboard_assignments')
    
    def form_valid(self, form):
        messages.success(self.request, f"Assignment '{form.instance.title}' updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

@login_required
def submission_detail(request, pk):
    """View submission details."""
    submission = get_object_or_404(Submission, pk=pk)
    context = {
        'submission': submission,
    }
    return render(request, 'assignments/submission_detail.html', context)

@login_required
def download_submission_file(request, pk):
    """Download a submission file."""
    submission = get_object_or_404(Submission, pk=pk)
    file_path = submission.file.path
    response = HttpResponse(open(file_path, 'rb').read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{submission.file.name}"'
    return response

@login_required
def api_assignments(request):
    """API endpoint to get all assignments."""
    assignments = Assignment.objects.all()
    data = {
        'assignments': [assignment.title for assignment in assignments]
    }
    return JsonResponse(data)

@login_required
def api_submissions(request):
    """API endpoint to get all submissions."""
    submissions = Submission.objects.all()
    data = {
        'submissions': [
            {
                'id': submission.id,
                'assignment': submission.assignment.title,
                'student': submission.student.username,
                'status': submission.status,
                'grade': submission.grade,
            } for submission in submissions
        ]
    }
    return JsonResponse(data)

@login_required
def api_submission_detail(request, pk):
    """API endpoint to get a single submission detail."""
    submission = get_object_or_404(Submission, pk=pk)
    data = {
        'id': submission.id,
        'assignment': submission.assignment.title,
        'student': submission.student.username,
        'status': submission.status,
        'grade': submission.grade,
    }
    return JsonResponse(data)

@login_required
def api_create_submission(request):
    """API endpoint to create a new submission."""
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.save()
            data = {
                'message': 'Submission created successfully.',
                'submission_id': submission.id
            }
            return JsonResponse(data, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)