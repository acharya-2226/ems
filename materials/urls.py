from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.dashboard_materials, name='dashboard'),
    path('upload/', views.upload_material, name='upload_material'),
    path('view/', views.view_materials, name='view_materials'),
    path('insights/', views.insights_materials, name='insights_materials'),
    path('edit/<int:pk>/', views.edit_material, name='edit_material'),
    path('delete/<int:pk>/', views.delete_material, name='delete_material'),
]