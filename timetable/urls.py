from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.dashboard_timetable, name='dashboard'),
    path('create/', views.create_timetable, name='create_timetable'),
    path('view/', views.view_timetable, name='view_timetable'),
    path('download/', views.download_timetable, name='download_timetable'),
    path('edit/<int:pk>/', views.edit_timetable, name='edit_timetable'),
    path('delete/<int:pk>/', views.delete_timetable, name='delete_timetable'),
    path('export/', views.export_timetable, name='export_timetable'),
]
