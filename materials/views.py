from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MaterialForm
from .models import Material


@login_required
def dashboard_materials(request):
    materials = Material.objects.all().order_by('-uploaded_at')
    return render(request, 'materials/dashboard_materials.html', {'materials': materials})


@login_required
def upload_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('materials:dashboard')
    else:
        form = MaterialForm()
    return render(request, 'materials/upload_material.html', {'form': form})


@login_required
def view_materials(request):
    materials = Material.objects.all().order_by('-uploaded_at')
    return render(request, 'materials/view_materials.html', {'materials': materials})


@login_required
def insights_materials(request):
    # Placeholder for analytics or insights about materials
    return render(request, 'materials/insights_materials.html')
