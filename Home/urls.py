"""
URL configuration for Home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from student import views as student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')),  # Include the school app's URLs
    path('student/', include("student.urls")),
    # Use the project's custom login/logout views to ensure consistent behavior
    path('login/', student_views.login_view, name='login'),
    path('logout/', student_views.logout_view, name='logout'),
    path('forgot-password/', PasswordResetView.as_view(template_name='forgot-password.html'), name='forgot-password'),  # Forgot Password URL
    # Include Django's auth URL patterns (password reset confirm, complete, etc.)
    # keep default auth urls but map accounts/login to our custom view for consistency
    path('accounts/login/', student_views.login_view, name='accounts_login'),
    path('accounts/', include('django.contrib.auth.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)