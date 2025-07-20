from django.http import HttpResponse
from django.urls import get_resolver
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return render(request, 'dashboard.html')  # Properly return an HttpResponse

def show_all_urls(request):
    resolver = get_resolver()
    url_list = resolver.reverse_dict.keys()
    html = "<h2>Registered URLs:</h2><ul style='font-family: monospace;'>"
    for url in sorted(url_list):
        if isinstance(url, str):
            html += f"<li>/{url}</li>"
    html += "</ul>"
    return HttpResponse(html)
