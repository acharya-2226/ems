from django.shortcuts import render

def dashboard_users(request):
    return render(request, 'users/dashboard_users.html')

def add_user(request):
    return render(request, 'users/add_user.html')

def view_users(request):
    return render(request, 'users/view_users.html')

def roles_permissions(request):
    # Placeholder view, update with your logic
    return render(request, 'users/user_role.html')

# def edit_user(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('users:view_users')
#     else:
#         form = UserChangeForm(instance=user)
#     return render(request, 'users/edit_user.html', {'form': form})