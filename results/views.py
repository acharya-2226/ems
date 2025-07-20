from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from .forms import ResultForm
from .models import Result, Student, Subject


@login_required
def dashboard_results(request):
    # Get some statistics for the dashboard
    total_results = Result.objects.count()
    published_results = Result.objects.filter(published=True).count()
    
    context = {
        'total_results': total_results,
        'published_results': published_results,
    }
    return render(request, 'results/dashboard_results.html', context)


@login_required
def publish_results(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save()
            messages.success(request, f'Result for {result.student} in {result.subject} has been successfully added!')
            return redirect('results:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResultForm()
    
    context = {'form': form}
    return render(request, 'results/publish_results.html', context)


@login_required
def view_results(request):
    results = Result.objects.select_related('student__user', 'subject').order_by('-created_at')
    
    # Filter options
    search_query = request.GET.get('search', '')
    semester_filter = request.GET.get('semester', '')
    year_filter = request.GET.get('year', '')
    published_filter = request.GET.get('published', '')
    
    if search_query:
        results = results.filter(
            Q(student__user__first_name__icontains=search_query) |
            Q(student__user__last_name__icontains=search_query) |
            Q(student__roll_number__icontains=search_query) |
            Q(subject__name__icontains=search_query) |
            Q(subject__code__icontains=search_query)
        )
    
    if semester_filter:
        results = results.filter(semester=semester_filter)
    
    if year_filter:
        results = results.filter(year=year_filter)
    
    if published_filter:
        results = results.filter(published=published_filter == 'true')
    
    # Get unique values for filters
    semesters = Result.objects.values_list('semester', flat=True).distinct().order_by('semester')
    years = Result.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'results': results,
        'semesters': semesters,
        'years': years,
        'search_query': search_query,
        'semester_filter': semester_filter,
        'year_filter': year_filter,
        'published_filter': published_filter,
    }
    return render(request, 'results/view_results.html', context)


@login_required
def edit_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            updated_result = form.save()
            messages.success(request, f'Result for {updated_result.student} in {updated_result.subject} has been updated!')
            return redirect('results:view_results')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResultForm(instance=result)
    
    context = {'form': form, 'result': result}
    return render(request, 'results/edit_results.html', context)


@login_required
def delete_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    
    if request.method == 'POST':
        student_name = result.student.user.get_full_name()
        subject_name = result.subject.name
        result.delete()
        messages.success(request, f'Result for {student_name} in {subject_name} has been deleted!')
        return redirect('results:view_results')
    
    context = {'result': result}
    return render(request, 'results/confirm_delete.html', context)


@login_required
def report_results(request):
    # Generate comprehensive reports
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_results = Result.objects.count()
    published_results = Result.objects.filter(published=True).count()
    
    # Grade distribution
    grade_distribution = Result.objects.values('grade').annotate(count=Count('grade')).order_by('grade')
    
    # Subject-wise average
    subject_averages = Result.objects.values('subject__name').annotate(
        avg_marks=Avg('marks_obtained'),
        count=Count('id')
    ).order_by('-avg_marks')
    
    # Recent results
    recent_results = Result.objects.select_related('student__user', 'subject').order_by('-created_at')[:10]
    
    # Top performers
    top_performers = Result.objects.filter(published=True).select_related('student__user', 'subject').order_by('-marks_obtained')[:10]
    
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_results': total_results,
        'published_results': published_results,
        'grade_distribution': grade_distribution,
        'subject_averages': subject_averages,
        'recent_results': recent_results,
        'top_performers': top_performers,
    }
    return render(request, 'results/report_results.html', context)