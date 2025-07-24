from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, show_all_urls
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='dashboard'),

    # App-specific URLs
    path('accounts/', include('accounts.urls')),  # Custom accounts app
    path('accounts/', include('allauth.urls')),  # Use allauth for authentication
    
    # Authentication - Use your custom views instead of Django's built-in ones
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    
    # Other app URLs

    path('attendance/', include('attendance.urls')),
    path('results/', include('results.urls')),
    path('assignments/', include('assignments.urls')),
    path('timetable/', include('timetable.urls')),
    path('materials/', include('materials.urls')),

    # path('users/', include('users.urls')),
    
    path('help/', TemplateView.as_view(template_name='help.html'), name='help'),  # static help page

    # Developer tool
    path('show-all-urls/', staff_member_required(show_all_urls), name='show_all_urls'),

    # NOTE: Remove duplicate includes below - they conflict with your custom accounts app
    # path('accounts/', include('django.contrib.auth.urls')),  # REMOVE - conflicts with accounts.urls
    # path('accounts/', include('allauth.urls')),              # REMOVE - not needed unless using allauth
]

# Media file handling in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)