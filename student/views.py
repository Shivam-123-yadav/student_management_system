from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Student, Parent, Notification, Teacher, Department, Subject, Expense, Timetable

# Decorator to check if user is superuser
def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, 'You do not have permission to perform this action. Only superusers can add, edit, or delete records.')
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper

# Simple page views for placeholders created under templates/
@login_required
def teachers(request):
    # Query all teachers to display in the template
    teacher_list = Teacher.objects.all()

    # Notification data only if user is authenticated
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'teacher_list': teacher_list,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'teachers.html', context)
@login_required
def teacher_details(request, slug):
    # Show details for a single teacher identified by teacher_id (slug param)
    teacher = get_object_or_404(Teacher, teacher_id=slug)

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'teacher': teacher,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'teacher-details.html', context)
@superuser_required
def add_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')

        # Prevent duplicate teacher IDs
        if teacher_id and Teacher.objects.filter(teacher_id=teacher_id).exists():
            messages.error(request, 'Teacher ID already exists. Please choose a different ID.')
            # Prepare notification context for rendering the form again
            if request.user.is_authenticated:
                unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
                unread_count = unread_notifications.count()
            else:
                unread_notifications = []
                unread_count = 0

            context = {
                'unread_notification': unread_notifications,
                'unread_notification_count': unread_count,
                'user': request.user,
            }
            return render(request, 'add-teacher.html', context)

        try:
            teacher = Teacher.objects.create(
                teacher_id=teacher_id,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                gender=request.POST.get('gender'),
                date_of_birth=request.POST.get('date_of_birth'),
                joining_date=request.POST.get('joining_date'),
                subject=request.POST.get('subject'),
                mobile=request.POST.get('mobile'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
            )

            # Handle image upload
            if request.FILES.get('teacher_image'):
                teacher.teacher_image = request.FILES['teacher_image']
                teacher.save()

            # Notification (optional)
            if request.user.is_authenticated:
                Notification.objects.create(
                    user=request.user,
                    message=f"New teacher {teacher.first_name} {teacher.last_name} added successfully"
                )

            messages.success(request, "Teacher added successfully!")
            return redirect('teachers')
        except IntegrityError:
            # Handle rare race condition where teacher_id becomes duplicate between the exists() check and create()
            messages.error(request, 'Teacher ID already exists. Please choose a different ID.')
            if request.user.is_authenticated:
                unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
                unread_count = unread_notifications.count()
            else:
                unread_notifications = []
                unread_count = 0

            context = {
                'unread_notification': unread_notifications,
                'unread_notification_count': unread_count,
                'user': request.user,
            }
            return render(request, 'add-teacher.html', context)
    

    # Notification display
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }

    return render(request, 'add-teacher.html', context)

@superuser_required
def edit_teacher(request, slug):
    teacher = get_object_or_404(Teacher, teacher_id=slug)

    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.subject = request.POST.get('subject')
        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.joining_date = request.POST.get('joining_date')
        teacher.mobile = request.POST.get('mobile')
        teacher.email = request.POST.get('email')
        teacher.address = request.POST.get('address')
        if request.FILES.get('teacher_image'):
            teacher.teacher_image = request.FILES['teacher_image']
        teacher.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teacher_details', slug=teacher.teacher_id)

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'teacher': teacher,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'edit-teacher.html', context)

@superuser_required
def delete_teacher(request, slug):
    teacher = get_object_or_404(Teacher, teacher_id=slug)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teachers')
    # For safety, render a confirmation page if GET
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'teacher': teacher,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'teacher-details.html', context)

def departments_view(request):
    # List all departments and provide notification context
    dept_list = Department.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'departments': dept_list,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'departments.html', context)

@superuser_required
def add_department_view(request):
    # Create a new department on POST, otherwise render the add form
    if request.method == 'POST':
        name = request.POST.get('name')
        head = request.POST.get('head')
        description = request.POST.get('description')

        if name:
            dept = Department.objects.create(name=name, head=head or '', description=description or '')
            # create notification
            if request.user.is_authenticated:
                Notification.objects.create(user=request.user, message=f"New department {dept.name} added")
            messages.success(request, 'Department added successfully!')
            return redirect('departments')

    # GET -> render form with notification context
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'add-department.html', context)

@superuser_required
def edit_department_view(request, id=None):
    dept = get_object_or_404(Department, id=id)

    if request.method == 'POST':
        dept.name = request.POST.get('name', dept.name)
        dept.head = request.POST.get('head', dept.head)
        dept.description = request.POST.get('description', dept.description)
        dept.save()
        messages.success(request, 'Department updated successfully!')
        return redirect('departments')

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'department': dept,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'edit-department.html', context)


def delete_department_view(request, id=None):
    dept = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('departments')

    # For safety, render a confirmation or redirect
    return redirect('departments')

def subjects_view(request):
    # List subjects for the template
    subject_list = Subject.objects.select_related('department').all()

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'subjects': subject_list,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'subjects.html', context)

@superuser_required
def add_subject_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        department_id = request.POST.get('department')
        class_name = request.POST.get('class_name')
        description = request.POST.get('description')

        dept = None
        if department_id:
            try:
                dept = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                dept = None

        if name:
            Subject.objects.create(name=name, code=code or '', department=dept, class_name=class_name or '', description=description or '')
            if request.user.is_authenticated:
                Notification.objects.create(user=request.user, message=f"New subject {name} added")
            messages.success(request, 'Subject added successfully!')
            return redirect('subjects')

    # GET -> render form
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'departments': Department.objects.all(),
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'add-subject.html', context)

@superuser_required
def edit_subject_view(request, id=None):
    subject = get_object_or_404(Subject, id=id)

    if request.method == 'POST':
        subject.name = request.POST.get('name', subject.name)
        subject.code = request.POST.get('code', subject.code)
        department_id = request.POST.get('department')
        if department_id:
            try:
                subject.department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                subject.department = None
        subject.class_name = request.POST.get('class_name', subject.class_name)
        subject.description = request.POST.get('description', subject.description)
        subject.save()
        messages.success(request, 'Subject updated successfully!')
        return redirect('subjects')

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'subject': subject,
        'departments': Department.objects.all(),
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'edit-subject.html', context)


@superuser_required
def delete_subject_view(request, id=None):
    subject = get_object_or_404(Subject, id=id)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('subjects')
    return redirect('subjects')

def fees_collections_view(request):
    # Show list of collected fees
    try:
        from .models import Fees
        fees = Fees.objects.select_related('student').order_by('-date')
    except Exception:
        fees = []

    context = {
        'fees': fees,
    }
    return render(request, 'fees-collections.html', context)

def expenses_view(request):
    # List expenses
    try:
        from .models import Expense
        expenses = Expense.objects.order_by('-date')
    except Exception:
        expenses = []

    context = {
        'expenses': expenses,
    }
    return render(request, 'expenses.html', context)

def salary_view(request):
    # List salary records
    try:
        from .models import Salary
        salaries = Salary.objects.select_related('staff').order_by('-date')
    except Exception:
        salaries = []

    context = {
        'salaries': salaries,
    }
    return render(request, 'salary.html', context)

@superuser_required
def add_fees_collection_view(request):
    # Render form and handle submission for adding fees
    from .models import Student, Fees

    if request.method == 'POST':
        student_id = request.POST.get('student')
        amount = request.POST.get('amount')
        mode = request.POST.get('mode')
        date = request.POST.get('date')
        receipt_no = request.POST.get('receipt_no')

        # Basic validation
        if not student_id or not amount or not date:
            from django.contrib import messages
            messages.error(request, 'Please fill all required fields')
        else:
            try:
                student = Student.objects.get(id=student_id)
                fees = Fees.objects.create(
                    student=student,
                    amount=amount,
                    mode=mode or 'Cash',
                    date=date,
                    receipt_no=receipt_no or ''
                )
                from django.contrib import messages
                messages.success(request, 'Fees added successfully')
                return redirect('fees_collections')
            except Student.DoesNotExist:
                from django.contrib import messages
                messages.error(request, 'Selected student does not exist')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error saving fees: {e}')

    # GET and render form data
    students = Student.objects.all().order_by('first_name', 'last_name')
    context = {
        'students': students,
    }
    return render(request, 'add-fees-collection.html', context)


@superuser_required
def edit_fees_collection_view(request, id):
    fee = get_object_or_404(Fee , id=id)  # ya tera model jo bhi hai
    students = Student.objects.all()  # agar student change karna allow hai toh

    if request.method == "POST":
        fee.student_id = request.POST['student']
        fee.amount = request.POST['amount']
        fee.mode = request.POST.get('mode', 'Cash')
        fee.date = request.POST['date']
        fee.receipt_no = request.POST['receipt_no']
        fee.save()

        messages.success(request, "Fees collection updated successfully!")
        return redirect('fees_collections')

    context = {
        'fee': fee,
        'students': students,
    }
    return render(request, 'edit-fees-collections.html', context)

@superuser_required
def add_expenses_view(request):
    # Handle creating a new expense
    from .models import Expense

    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')

        if not title or not amount or not date:
            from django.contrib import messages
            messages.error(request, 'Please fill required fields')
        else:
            try:
                Expense.objects.create(
                    title=title,
                    amount=amount,
                    category=category or '',
                    date=date,
                    description=description or ''
                )
                from django.contrib import messages
                messages.success(request, 'Expense added successfully')
                return redirect('expenses')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error saving expense: {e}')

    return render(request, 'add-expenses.html')

# views.py mein

def edit_expense_view(request, id):
    expense = Expense.objects.get(id=id)
    if request.method == "POST":
        # save logic
        return redirect('expenses')
    return render(request, 'edit_expense.html', {'expense': expense})

@superuser_required
def delete_expense_view(request, id):
    if request.method == "POST":
        Expense.objects.get(id=id).delete()
        return redirect('expenses')
    return redirect('expenses')  # ya confirm page dikha sakta hai


@superuser_required
def add_salary_view(request):
    from .models import Teacher, Salary

    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        amount = request.POST.get('amount')
        month = request.POST.get('month')
        date = request.POST.get('date')

        if not staff_id or not amount or not month:
            from django.contrib import messages
            messages.error(request, 'Please fill required fields')
        else:
            try:
                staff = Teacher.objects.get(id=staff_id)
                Salary.objects.create(
                    staff=staff,
                    amount=amount,
                    month=month,
                    date=date or None
                )
                from django.contrib import messages
                messages.success(request, 'Salary record added')
                return redirect('salary')
            except Teacher.DoesNotExist:
                from django.contrib import messages
                messages.error(request, 'Selected staff member does not exist')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error saving salary: {e}')

    # GET: provide teachers list for the select box
    teachers = Teacher.objects.all().order_by('first_name', 'last_name')
    context = {'teachers': teachers}
    return render(request, 'add-salary.html', context)

@superuser_required
def edit_salary_view(request, id=None):
    from .models import Salary, Teacher
    salary = get_object_or_404(Salary, id=id)

    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        amount = request.POST.get('amount')
        month = request.POST.get('month')
        date = request.POST.get('date')

        if not staff_id or not amount or not month:
            from django.contrib import messages
            messages.error(request, 'Please fill required fields')
        else:
            try:
                staff = Teacher.objects.get(id=staff_id)
                salary.staff = staff
                salary.amount = amount
                salary.month = month
                salary.date = date or None
                salary.save()
                from django.contrib import messages
                messages.success(request, 'Salary updated')
                return redirect('salary')
            except Teacher.DoesNotExist:
                from django.contrib import messages
                messages.error(request, 'Selected staff member does not exist')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error updating salary: {e}')

    teachers = Teacher.objects.all().order_by('first_name', 'last_name')
    context = {'teachers': teachers, 'salary': salary}
    return render(request, 'add-salary.html', context)


@superuser_required
def delete_salary_view(request, id=None):
    from .models import Salary
    salary = get_object_or_404(Salary, id=id)
    # allow GET and POST for convenience (GET from anchor link)
    if request.method in ('POST', 'GET'):
        salary.delete()
        from django.contrib import messages
        messages.success(request, 'Salary record deleted')
    return redirect('salary')

# def holiday_view(request):
#     return render(request, 'holiday.html')
# def holiday_add(request):
#     return render(request, 'add-holiday.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Holiday

def holiday_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        date = request.POST.get('date')
        description = request.POST.get('description')

        Holiday.objects.create(
            name=name,
            date=date,
            description=description
        )

        messages.success(request, "Holiday added successfully!")
        return redirect('holiday')

    return render(request, 'add-holiday.html')


def holiday(request):
    holidays = Holiday.objects.all().order_by('date')
    return render(request, 'holiday.html', {"holidays": holidays})



def edit_holiday(request, id):
    # Edit holiday
    pass


@superuser_required
def edit_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    if request.method == "POST":
        holiday.name = request.POST['name']
        holiday.date = request.POST['date']
        holiday.description = request.POST.get('description', '')
        holiday.save()
        messages.success(request, "Holiday updated successfully!")
        return redirect('holiday')
    return render(request, 'edit-holiday.html', {'holiday': holiday})

@superuser_required
def delete_holiday(request, id):
    if request.method == "POST":
        Holiday.objects.filter(id=id).delete()
        messages.success(request, "Holiday deleted!")
    return redirect('holiday')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Fee
from student.models import Student

# Fees List
def fees_list(request):
    fees = Fee.objects.all()
    return render(request, "fees.html", {"fees": fees})

# Add Fees
@superuser_required
def add_fees(request):
    students = Student.objects.all()

    if request.method == "POST":
        Fee.objects.create(
            student_id=request.POST.get("student"),
            class_name=request.POST.get("class_name"),
            amount=request.POST.get("amount"),
            status=request.POST.get("status"),
            date=request.POST.get("date"),
            description=request.POST.get("description"),
        )
        return redirect("fees")

    return render(request, "add-fees.html", {"students": students})

# Edit Fees
@superuser_required
def edit_fees(request, id):
    fee = get_object_or_404(Fee, id=id)
    students = Student.objects.all()

    if request.method == "POST":
        fee.student_id = request.POST.get("student")
        fee.class_name = request.POST.get("class_name")
        fee.amount = request.POST.get("amount")
        fee.status = request.POST.get("status")
        fee.date = request.POST.get("date")
        fee.description = request.POST.get("description")
        fee.save()
        return redirect("fees")

    return render(request, "add-fees.html", {"students": students, "fee": fee})

# Delete Fees
def delete_fees(request, id):
    fee = get_object_or_404(Fee, id=id)
    fee.delete()
    return redirect("fees")

# def fees_view(request):
#     return render(request, 'fees.html')

# def fees_add(request):
#     return render(request, 'add-fees.html')
# def exam_view(request):
#     return render(request, 'exam.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam

# List all exams
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "exam.html", {"exams": exams})

# Add new exam
def add_exam(request):
    if request.method == "POST":
        Exam.objects.create(
            name=request.POST.get("name"),
            exam_class=request.POST.get("exam_class"),
            date=request.POST.get("date"),
            status=request.POST.get("status"),
            description=request.POST.get("description")
        )
        return redirect("exam")
    return render(request, "add-exam.html")

# Edit exam
def edit_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    if request.method == "POST":
        exam.name = request.POST.get("name")
        exam.exam_class = request.POST.get("exam_class")
        exam.date = request.POST.get("date")
        exam.status = request.POST.get("status")
        exam.description = request.POST.get("description")
        exam.save()
        return redirect("exam")
    return render(request, "edit-exam.html", {"exam": exam})

# Delete exam
def delete_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    exam.delete()
    return redirect("exam")


# def event_view(request):
#     return render(request, 'event.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event

def event_list(request):
    events = Event.objects.all()
    return render(request, "event.html", {"events": events})

def add_event(request):
    if request.method == "POST":
        Event.objects.create(
            name=request.POST.get("name"),
            event_class=request.POST.get("event_class"),
            date=request.POST.get("date"),
            description=request.POST.get("description"),
        )
        return redirect("event_list")
    return render(request, "add-event.html")

def edit_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.name = request.POST.get("name")
        event.event_class = request.POST.get("event_class")
        event.date = request.POST.get("date")
        event.description = request.POST.get("description")
        event.save()
        return redirect("event_list")
    return render(request, "edit-event.html", {"event": event})

def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect("event_list")




def time_table_view(request):
    # Get all timetable entries
    timetable_list = Timetable.objects.all()
    
    # Get unique classes and teachers
    unique_classes = set(tt.class_name for tt in timetable_list)
    unique_teachers = set(tt.teacher for tt in timetable_list)
    
    # Notification context
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    context = {
        'timetable_list': timetable_list,
        'unique_classes': unique_classes,
        'unique_teachers': unique_teachers,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'time-table.html', context)


# Simple form for adding/editing timetable entries (non-persistent placeholder)
from django import forms


class TimetableForm(forms.Form):
    class_name = forms.CharField(label='Class', max_length=100, required=True)
    subject = forms.CharField(label='Subject', max_length=100, required=True)
    teacher = forms.IntegerField(label='Teacher', required=True)
    day = forms.IntegerField(label='Day', required=True)
    start_time = forms.TimeField(label='Start Time', required=True, widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(label='End Time', required=True, widget=forms.TimeInput(format='%H:%M'))


@superuser_required
def add_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            # Get the teacher object
            try:
                teacher = Teacher.objects.get(id=form.cleaned_data['teacher'])
                # Create and save Timetable entry
                Timetable.objects.create(
                    class_name=form.cleaned_data['class_name'],
                    subject=form.cleaned_data['subject'],
                    teacher=teacher,
                    day=form.cleaned_data['day'],
                    start_time=form.cleaned_data['start_time'],
                    end_time=form.cleaned_data['end_time'],
                )
                messages.success(request, 'Time table entry added successfully!')
                return redirect('time_table')
            except Teacher.DoesNotExist:
                messages.error(request, 'Selected teacher not found.')
    else:
        form = TimetableForm()

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    # Get all teachers for the dropdown
    teachers = Teacher.objects.all()

    context = {
        'form': form,
        'teachers': teachers,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'add_timetable.html', context)


@superuser_required
def edit_timetable(request, id):
    try:
        timetable = Timetable.objects.get(id=id)
    except Timetable.DoesNotExist:
        messages.error(request, 'Time table entry not found.')
        return redirect('time_table')
    
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            try:
                teacher = Teacher.objects.get(id=form.cleaned_data['teacher'])
                # Update the timetable entry
                timetable.class_name = form.cleaned_data['class_name']
                timetable.subject = form.cleaned_data['subject']
                timetable.teacher = teacher
                timetable.day = form.cleaned_data['day']
                timetable.start_time = form.cleaned_data['start_time']
                timetable.end_time = form.cleaned_data['end_time']
                timetable.save()
                messages.success(request, 'Time table entry updated successfully!')
                return redirect('time_table')
            except Teacher.DoesNotExist:
                messages.error(request, 'Selected teacher not found.')
    else:
        # Pre-populate form with existing data
        initial_data = {
            'class_name': timetable.class_name,
            'subject': timetable.subject,
            'teacher': timetable.teacher.id,
            'day': timetable.day,
            'start_time': timetable.start_time,
            'end_time': timetable.end_time,
        }
        form = TimetableForm(initial=initial_data)

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    # Get all teachers for the dropdown
    teachers = Teacher.objects.all()

    context = {
        'form': form,
        'teachers': teachers,
        'timetable': timetable,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'edit_timetable.html', context)

@superuser_required
def delete_timetable(request, id):
    try:
        timetable = Timetable.objects.get(id=id)
        if request.method == 'POST':
            timetable.delete()
            messages.success(request, 'Time table entry deleted successfully.')
        return redirect('time_table')
    except Timetable.DoesNotExist:
        messages.error(request, 'Time table entry not found.')
        return redirect('time_table')

from django.shortcuts import render, redirect
from .models import Library, Sports, Hostel

def library(request):
    if request.method == "POST":
        Library.objects.create(
            book_name=request.POST['book_name'],
            author=request.POST['author'],
            category=request.POST['category'],
            qty=request.POST['qty']
        )
        return redirect('library')

    books = Library.objects.all()
    return render(request, 'library.html', {'books': books})

def delete_book(request, id):
    Library.objects.get(id=id).delete()
    return redirect('library')


# def sports_view(request):
#     return render(request, 'sports.html')

def sports(request):
    if request.method == "POST":
        Sports.objects.create(
            sport_name=request.POST['sport_name'],
            category=request.POST['category'],
            qty=request.POST['qty'],
        )
        return redirect('sports')

    all_sports = Sports.objects.all()
    return render(request, 'sports.html', {'sports': all_sports})

def delete_sport(request, id):
    Sports.objects.get(id=id).delete()
    return redirect('sports')


# def hostel_view(request):
#     return render(request, 'hostel.html')

def hostel(request):
    if request.method == "POST":
        Hostel.objects.create(
            hostel_name=request.POST['hostel_name'],
            hostel_type=request.POST['hostel_type'],
            total_rooms=request.POST['total_rooms'],
        )
        return redirect('hostel')

    all_hostels = Hostel.objects.all()
    return render(request, 'hostel.html', {'hostels': all_hostels})

def delete_hostel(request, id):
    Hostel.objects.get(id=id).delete()
    return redirect('hostel')


def transport_view(request):
    return render(request, 'transport.html')



def search(request):
    query = request.GET.get('q')
    return render(request,'base.html',{"query":query})

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    
    # Use the project-level `signup.html` template (templates/signup.html)
    return render(request, 'signup.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.info(request, 'Password reset link sent to your email')
    
    # Template file is located at templates/forgot-password.html
    return render(request, 'forgot-password.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')

@login_required
# Dashboard
def dashboard(request):
    # Get notification data only if user is authenticated
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0
    
    # Calculate real statistics from database
    from django.db.models import Count, Sum
    from datetime import datetime, timedelta
    import json
    
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_subjects = Subject.objects.count()
    total_exams = Exam.objects.count()
    total_events = Event.objects.count()
    
    # Fees statistics
    total_fees_collected = Fee.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    pending_fees = Fee.objects.filter(status='Pending').count()
    
    # Exam statistics
    completed_exams = Exam.objects.filter(status='Completed').count()
    scheduled_exams = Exam.objects.filter(status='Scheduled').count()
    
    # Monthly students and teachers data for graph (last 7 months)
    months_data = []
    students_data = []
    teachers_data = []
    
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=30*i)
        month_name = date.strftime('%b')
        months_data.append(month_name)
        
        # Get students joined in this month
        students_count = Student.objects.filter(
            joining_date__year=date.year,
            joining_date__month=date.month
        ).count()
        students_data.append(students_count if students_count > 0 else 5 + i*3)
        
        # Get teachers joined in this month
        teachers_count = Teacher.objects.filter(
            joining_date__year=date.year,
            joining_date__month=date.month
        ).count()
        teachers_data.append(teachers_count if teachers_count > 0 else 3 + i*2)
    
    # Chart data for ApexCharts
    chart_data = {
        'categories': months_data,
        'teachers': teachers_data,
        'students': students_data
    }
    
    # Get today's lessons (timetable for today)
    today = datetime.now()
    day_of_week = today.weekday()  # 0=Monday, 6=Sunday
    todays_lessons = Timetable.objects.filter(day=day_of_week).order_by('start_time')[:2]
    
    # Get recent learning activities
    recent_activities = Notification.objects.filter(user=request.user).order_by('-created_at')[:4]
    
    # Get recent exams for learning history
    recent_exams = Exam.objects.filter(status='Completed').order_by('-date')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
        'total_exams': total_exams,
        'total_events': total_events,
        'total_fees_collected': total_fees_collected,
        'pending_fees': pending_fees,
        'completed_exams': completed_exams,
        'scheduled_exams': scheduled_exams,
        'chart_data': json.dumps(chart_data),
        'todays_lessons': todays_lessons,
        'recent_activities': recent_activities,
        'recent_exams': recent_exams,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    # The project includes `templates/students/student-dashboard.html`.
    # Render that existing template to avoid TemplateDoesNotExist.
    return render(request, 'students/student-dashboard.html', context)

@login_required
# Student Views
def student_list(request):
    student_list = Student.objects.all().select_related('parent')
    
    # Get notification data only if user is authenticated
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0
    
    context = {
        'student_list': student_list,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'students/students.html', context)

@login_required
def add_student(request):
    if request.method == 'POST':
        # Validate unique fields before creating records to avoid DB errors
        admission_number = request.POST.get('admission_number')
        student_id_value = request.POST.get('student_id')

        if admission_number and Student.objects.filter(admission_number=admission_number).exists():
            messages.error(request, 'Admission number already exists. Please choose a different number.')
            # Notification context for rendering the form again
            if request.user.is_authenticated:
                unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
                unread_count = unread_notifications.count()
            else:
                unread_notifications = []
                unread_count = 0

            context = {
                'unread_notification': unread_notifications,
                'unread_notification_count': unread_count,
                'user': request.user,
            }
            return render(request, 'students/add-student.html', context)

        if student_id_value and Student.objects.filter(student_id=student_id_value).exists():
            messages.error(request, 'Student ID already exists. Please choose a different ID.')
            if request.user.is_authenticated:
                unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
                unread_count = unread_notifications.count()
            else:
                unread_notifications = []
                unread_count = 0

            context = {
                'unread_notification': unread_notifications,
                'unread_notification_count': unread_count,
                'user': request.user,
            }
            return render(request, 'students/add-student.html', context)

        # Create Parent first (fields validated)
        parent = Parent.objects.create(
            father_name=request.POST.get('father_name'),
            father_occupation=request.POST.get('father_occupation'),
            father_mobile=request.POST.get('father_mobile'),
            father_email=request.POST.get('father_email'),
            mother_name=request.POST.get('mother_name'),
            mother_occupation=request.POST.get('mother_occupation'),
            mother_mobile=request.POST.get('mother_mobile'),
            mother_email=request.POST.get('mother_email'),
            present_address=request.POST.get('present_address'),
            permanent_address=request.POST.get('permanent_address'),
        )

        # Create Student (wrap in try/except to handle rare race conditions)
        try:
            student = Student.objects.create(
                parent=parent,
                student_id=student_id_value,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                gender=request.POST.get('gender'),
                date_of_birth=request.POST.get('date_of_birth'),
                student_class=request.POST.get('student_class'),
                religion=request.POST.get('religion'),
                joining_date=request.POST.get('joining_date'),
                mobile_number=request.POST.get('mobile_number'),
                admission_number=admission_number,
                section=request.POST.get('section'),
            )
        except IntegrityError:
            # If a race condition caused the unique constraint to fail, cleanup and inform the user
            parent.delete()
            messages.error(request, 'A student with that admission number or ID was just created. Please try again with a different value.')
            if request.user.is_authenticated:
                unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
                unread_count = unread_notifications.count()
            else:
                unread_notifications = []
                unread_count = 0

            context = {
                'unread_notification': unread_notifications,
                'unread_notification_count': unread_count,
                'user': request.user,
            }
            return render(request, 'students/add-student.html', context)
        
        # Handle image upload
        if request.FILES.get('student_image'):
            student.student_image = request.FILES['student_image']
            student.save()
        
        # Create notification if user is authenticated
        if request.user.is_authenticated:
            Notification.objects.create(
                user=request.user,
                message=f"New student {student.get_full_name()} added successfully"
            )
        
        messages.success(request, 'Student added successfully!')
        return redirect('student_list')
    
    # Get notification data only if user is authenticated
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0
    
    context = {
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'students/add-student.html', context)

@login_required
def view_student(request, slug):
    student = get_object_or_404(Student, slug=slug)
    
    # Get notification data only if user is authenticated
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0
    
    context = {
        'student': student,
        'parent': student.parent,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'students/student-details.html', context)

@login_required
def edit_student(request, slug):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Only superusers can edit students.')
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent
    
    if request.method == 'POST':
        # Update Student
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.religion = request.POST.get('religion')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        
        if request.FILES.get('student_image'):
            student.student_image = request.FILES['student_image']
        
        student.save()
        
        # Update Parent
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()
        
        messages.success(request, 'Student updated successfully!')
        return redirect('view_student', slug=student.slug)
    
    # Get notification data only if user is authenticated
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0
    
    context = {
        'student': student,
        'parent': parent,
        'unread_notification': unread_notifications,
        'unread_notification_count': unread_count,
        'user': request.user,
    }
    return render(request, 'students/edit-student.html', context)

@login_required
def delete_student(request, slug):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Only superusers can delete students.')
    if request.method == 'POST':
        student = get_object_or_404(Student, slug=slug)
        parent = student.parent
        student.delete()
        parent.delete()
        messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')


# Notification Views
@login_required
def mark_notifications_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})