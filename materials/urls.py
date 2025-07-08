from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.dashboard_materials, name='dashboard'),
    path('upload/', views.upload_material, name='upload_material'),
    path('view/', views.view_materials, name='view_materials'),
    path('insights/', views.insights_materials, name='insights_materials'),
]
