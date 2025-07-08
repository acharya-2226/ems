from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('', views.dashboard_results, name='dashboard'),
    path('publish/', views.publish_results, name='publish_results'),
    path('view/', views.view_results, name='view_results'),
    path('report/', views.report_results, name='report_results'),
]
