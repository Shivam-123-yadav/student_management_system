from django.contrib import admin
from .models import Student, Parent, Notification, Teacher, Department, Fees, Expense
from . import models


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['father_name', 'mother_name', 'father_mobile', 'mother_mobile', 'created_at']
    search_fields = ['father_name', 'mother_name', 'father_email', 'mother_email']
    list_filter = ['created_at']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'student_class', 'section', 'mobile_number', 'created_at']
    search_fields = ['student_id', 'first_name', 'last_name', 'admission_number']
    list_filter = ['student_class', 'section', 'gender', 'created_at']
    prepopulated_fields = {'slug': ('student_id',)}


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'message']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'teacher_id',
        'first_name',
        'last_name',
        'subject',
        'mobile',
        'email'
    ]
    search_fields = ['teacher_id', 'first_name', 'last_name', 'mobile', 'email']
    list_filter = ['gender', 'subject']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'created_at']
    search_fields = ['name', 'head']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'mode', 'date', 'receipt_no')
    list_filter = ('mode', 'date')
    search_fields = ('student__first_name', 'student__last_name', 'receipt_no')
    ordering = ('-date',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'category')
    ordering = ('-date',)


@admin.register(models.Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'amount', 'month', 'date')
    list_filter = ('month', 'date')
    search_fields = ('staff__first_name', 'staff__last_name')
    ordering = ('-date',)

from django.contrib import admin
from .models import Fee

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'class_name', 'amount', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('student__name', 'class_name')


