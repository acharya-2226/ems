from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.dashboard_timetable, name='dashboard'),
    path('create/', views.create_timetable, name='create_timetable'),
    path('view/', views.view_timetable, name='view_timetable'),
     path('download/', views.download_timetable, name='download_timetable'),
]
