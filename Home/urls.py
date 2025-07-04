"""
URL configuration for Home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')),  # Include the school app's URLs
    path('student/', include("student.urls")),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Login URL
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout URL
    path('forgot-password/', PasswordResetView.as_view(template_name='forgot_password.html'), name='forgot-password'),  # Forgot Password URL
]
