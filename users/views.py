from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@login_required
def dashboard_users(request):
    """Dashboard landing page for user management."""
    total_users = CustomUser.objects.count()
    total_students = CustomUser.objects.filter(role='student').count()
    total_teachers = CustomUser.objects.filter(role='teacher').count()
    total_admins = CustomUser.objects.filter(role='admin').count()
    
    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_admins': total_admins,
    }
    return render(request, 'users/dashboard_users.html', context)


@login_required
def view_users(request):
    """List all users with pagination."""
    users_list = CustomUser.objects.all().order_by('username')
    paginator = Paginator(users_list, 10)  # Show 10 users per page
    
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'users/view_users.html', {'users': users})


@login_required
def add_user(request):
    """Add a new user."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully.")
            return redirect('users:view_users')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/add_user.html', {'form': form})


@login_required
def edit_user(request, user_id):
    """Edit an existing user."""
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('users:view_users')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})


@login_required
def delete_user(request, user_id):
    """Delete a user."""
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('users:view_users')
    return render(request, 'users/confirm_delete.html', {'user': user})


@login_required
def roles_permissions(request):
    """Manage user roles and permissions."""
    users_by_role = {
        'students': CustomUser.objects.filter(role='student'),
        'teachers': CustomUser.objects.filter(role='teacher'),
        'admins': CustomUser.objects.filter(role='admin'),
    }
    return render(request, 'users/user_role.html', {'users_by_role': users_by_role})


@login_required
def profile_view(request):
    """User profile page."""
    user = request.user
    return render(request, 'users/profile.html', {'user': user})


@login_required
def settings_view(request):
    """User settings page."""
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('users:settings')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/settings.html', {'form': form})