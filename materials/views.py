from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MaterialForm
from .models import Material

@login_required
def dashboard_materials(request):
    try:
        materials = Material.objects.all().order_by('-uploaded_at')
    except:
        materials = []
    return render(request, 'materials/dashboard_materials.html', {'materials': materials})

@login_required
def upload_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Material uploaded successfully.")
                return redirect('materials:dashboard')
            except:
                messages.error(request, "Error uploading material. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MaterialForm()
    return render(request, 'materials/upload_material.html', {'form': form})

@login_required
def view_materials(request):
    try:
        materials = Material.objects.all().order_by('-uploaded_at')
    except:
        materials = []
    return render(request, 'materials/view_materials.html', {'materials': materials})

@login_required
def insights_materials(request):
    try:
        total_materials = Material.objects.count()
        recent_materials = Material.objects.order_by('-uploaded_at')[:5]
    except:
        total_materials = 0
        recent_materials = []
    
    context = {
        'total_materials': total_materials,
        'recent_materials': recent_materials,
    }
    return render(request, 'materials/insights_materials.html', context)

@login_required
def edit_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Material updated successfully.")
                return redirect('materials:dashboard')
            except:
                messages.error(request, "Error updating material. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MaterialForm(instance=material)
    return render(request, 'materials/edit_materials.html', {'form': form, 'material': material})

@login_required
def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        try:
            material.delete()
            messages.success(request, "Material deleted successfully.")
        except:
            messages.error(request, "Error deleting material. Please try again.")
        return redirect('materials:dashboard')
    return render(request, 'materials/confirm_delete.html', {'material': material})