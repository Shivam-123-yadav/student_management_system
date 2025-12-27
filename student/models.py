from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import random
import string

class Parent(models.Model):
    father_name = models.CharField(max_length=200)
    father_occupation = models.CharField(max_length=200)
    father_mobile = models.CharField(max_length=15)
    father_email = models.EmailField()
    mother_name = models.CharField(max_length=200)
    mother_occupation = models.CharField(max_length=200)
    mother_mobile = models.CharField(max_length=15)
    mother_email = models.EmailField()
    present_address = models.TextField()
    permanent_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.father_name} / {self.mother_name}"


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')
    student_id = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    student_class = models.CharField(max_length=50)
    religion = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    admission_number = models.CharField(max_length=50, unique=True)
    section = models.CharField(max_length=10)
    student_image = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.student_id)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    teacher_image = models.ImageField(upload_to='teachers/', blank=True, null=True)


class Department(models.Model):
    name = models.CharField(max_length=200)
    head = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    class_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Fees(models.Model):
    PAYMENT_MODES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(max_length=30, choices=PAYMENT_MODES, default='Cash')
    date = models.DateField()
    receipt_no = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.amount} ({self.receipt_no})"


class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Salary(models.Model):
    staff = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='salaries')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # store month as YYYY-MM string (matches <input type="month">)
    month = models.CharField(max_length=7)
    date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.get_full_name() if hasattr(self.staff, 'get_full_name') else self.staff} - {self.month} - {self.amount}"

from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


from django.db import models
from student.models import Student

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_records')
    class_name = models.CharField(max_length=50)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=(('Paid','Paid'),('Pending','Pending')))
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.amount}"


from django.db import models

class Exam(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed')
    ]

    name = models.CharField(max_length=100)
    exam_class = models.CharField(max_length=50)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.exam_class}"

from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    event_class = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Library(models.Model):
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    qty = models.IntegerField()


class Sports(models.Model):
    sport_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    qty = models.IntegerField()


class Hostel(models.Model):
    hostel_name = models.CharField(max_length=200)
    hostel_type = models.CharField(max_length=100)
    total_rooms = models.IntegerField()


class Timetable(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    class_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetables')
    day = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_day_display(self):
        return dict(self.DAY_CHOICES).get(self.day, '')
    
    def __str__(self):
        return f"Class {self.class_name} - {self.subject} ({self.get_day_display()})"
    
    class Meta:
        ordering = ['day', 'start_time']

