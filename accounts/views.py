import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import xlwt
import xlrd
from django import forms
from .forms import (
    SignupForm, CustomAuthenticationForm, MicrosoftSignupForm,
    UserProfileForm, AdminUserForm
)
from .forms import ExcelImportForm

from .models import CustomUser
from .forms import (
    SignupForm, CustomAuthenticationForm, MicrosoftSignupForm, 
    UserProfileForm, AdminUserForm
)


# Authentication Views
def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Redirect based on user role
            if user.role == 'admin':
                return redirect('dashboard_users')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def signup_view(request):
    """Handle regular user registration."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_email_verified = False  # Set to False until email verification
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    
    context = {
        'form': form,
        'MICROSOFT_CLIENT_ID': getattr(settings, 'MICROSOFT_CLIENT_ID', None),
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(["POST"])
def microsoft_signup(request):
    """Handle Microsoft OAuth signup via AJAX."""
    try:
        data = json.loads(request.body)
        
        # Validate email domain
        email = data.get('email', '').lower()
        if not email.endswith('@hcoe.edu.np'):
            return JsonResponse({
                'success': False,
                'error': 'Only @hcoe.edu.np email addresses are allowed.'
            }, status=400)
        
        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'An account with this email already exists.'
            }, status=400)
        
        # Verify Microsoft token
        if not verify_microsoft_token(data.get('access_token')):
            return JsonResponse({
                'success': False,
                'error': 'Invalid Microsoft authentication token.'
            }, status=400)
        
        # Create user account
        username = email.split('@')[0]
        # Ensure unique username
        base_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            microsoft_id=data.get('microsoft_id'),
            roll_number=data.get('roll_number', ''),
            role=data.get('role', 'student'),
            is_active=True,
            is_email_verified=True,  # Microsoft users are pre-verified
        )
        
        # Log the user in
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Account created successfully!',
            'redirect_url': '/dashboard/'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Registration failed. Please try again.'
        }, status=500)


def microsoft_callback(request):
    """Handle Microsoft OAuth callback."""
    return render(request, 'accounts/microsoft_callback.html')


def verify_microsoft_token(access_token):
    """Verify Microsoft Graph API token."""
    if not access_token:
        return False
    
    try:
        response = requests.get(
            'https://graph.microsoft.com/v1.0/me',
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=10
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


# Dashboard Views
@login_required
def dashboard_view(request):
    """Main dashboard for regular users."""
    context = {
        'user': request.user,
        'recent_activities': [],  # Add your logic here
    }
    return render(request, 'accounts/dashboard.html', context)


# User Management Views (Admin only)
def is_admin(user):
    """Check if user is admin."""
    return user.is_authenticated and user.role == 'admin'


@user_passes_test(is_admin)
def dashboard_users(request):
    """Admin dashboard for managing users."""
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    
    users = CustomUser.objects.all()
    
    # Apply filters
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    users = users.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': CustomUser.ROLE_CHOICES,
        'total_users': CustomUser.objects.count(),
        'total_admins': CustomUser.objects.filter(role='admin').count(),
        'total_teachers': CustomUser.objects.filter(role='teacher').count(),
        'total_students': CustomUser.objects.filter(role='student').count(),
    }
    return render(request, 'accounts/dashboard_users.html', context)


@user_passes_test(is_admin)
def add_user(request):
    """Admin view to add new user."""
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('dashboard_users')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminUserForm()
    
    return render(request, 'accounts/add_user.html', {'form': form})


@user_passes_test(is_admin)
def edit_user(request, user_id):
    """Admin view to edit user."""
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('dashboard_users')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminUserForm(instance=user)
    
    return render(request, 'accounts/edit_user.html', {'form': form, 'user_obj': user})


@user_passes_test(is_admin)
def view_user(request, user_id):
    """Admin view to view user details."""
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'accounts/dashboard_users.html', {'user_obj': user})


@user_passes_test(is_admin)
def user_role(request, user_id):
    """Admin view to change user role."""
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in [choice[0] for choice in CustomUser.ROLE_CHOICES]:
            user.role = new_role
            user.save()
            messages.success(request, f'User role updated to {user.get_role_display()}!')
        else:
            messages.error(request, 'Invalid role selected.')
        return redirect('dashboard_users')
    
    return render(request, 'accounts/user_role.html', {
        'user_obj': user,
        'role_choices': CustomUser.ROLE_CHOICES
    })


@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Admin view to delete user."""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent deletion of self
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('dashboard_users')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('dashboard_users')
    
    return render(request, 'accounts/delete_user.html', {'user_obj': user})


# Profile Views
@login_required
def profile(request):
    """User profile view and edit."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def email_settings(request):
    """User email settings view."""
    return render(request, 'accounts/email_settings.html')



@login_required
def account_settings(request):
    """User account settings view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account settings updated successfully!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/settings.html', {'form': form})

@login_required
def customuser_download_format(request):
    """Download format for CustomUser import."""
    model_fields = [f.name for f in CustomUser._meta.fields if f.name not in ['id', 'password', 'last_login', 'date_joined']]
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=users_format.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Format')
    for col_num, field in enumerate(model_fields):
        ws.write(0, col_num, field)
    wb.save(response)
    return response


@login_required
def customuser_import_xls(request):
    """Import CustomUser data from Excel file."""
    if request.method == "POST":
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            book = xlrd.open_workbook(file_contents=excel_file.read())
            sheet = book.sheet_by_index(0)
            headers = [cell.value.strip() for cell in sheet.row(0)]
            success_count = 0
            for row_idx in range(1, sheet.nrows):
                row_data = {headers[col]: sheet.cell_value(row_idx, col) for col in range(len(headers))}
                try:
                    CustomUser.objects.create(**row_data)
                    success_count += 1
                except Exception as e:
                    messages.error(request, f"Row {row_idx + 1} error: {str(e)}")
            messages.success(request, f"{success_count} users successfully imported.")
            return redirect('dashboard_users')
    else:
        form = ExcelImportForm()

    context = {
        'form': form,
        'opts': CustomUser._meta,
    }
    return render(request, "admin/accounts/customuser/import_form.html", context)

@login_required
def roles_permissions(request):
    """User roles and permissions management."""
    return render(request, 'accounts/roles_permissions.html', {
        'role_choices': CustomUser.ROLE_CHOICES,
    })          

@login_required
def signup(request):
    return render(request, 'accounts/signup.html', {'form': form})  
