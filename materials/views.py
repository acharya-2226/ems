from django.shortcuts import render

def dashboard_materials(request):
    return render(request, 'materials/dashboard_materials.html')

def upload_material(request):
    return render(request, 'materials/upload_material.html')

def view_materials(request):
    return render(request, 'materials/view_materials.html')

def insights_materials(request):
    return render(request, 'materials/insights_materials.html')
