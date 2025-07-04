from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('signup/', views.signup, name='signup'),
    path('notifications/mark-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('notifications/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
]
