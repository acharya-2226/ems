from django.shortcuts import render

def dashboard_results(request):
    return render(request, 'results/dashboard_results.html')

def publish_results(request):
    return render(request, 'results/publish_results.html')

def view_results(request):
    return render(request, 'results/view_results.html')

def report_results(request):
    return render(request, 'results/report_results.html')