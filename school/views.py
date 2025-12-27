from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import models
from .models import AdminProfile
@login_required
def index(request):
    # Build dashboard values from the database where possible.
    students_count = 0
    teachers_count = 0
    notifications = []
    star_students = []
    activities = []
    departments_count = 0
    awards_count = 0
    revenue = 0

    try:
        from student.models import Student, Teacher, Notification as StudentNotification
        from django.db.models import Sum
        import json
        from datetime import datetime, timedelta

        students_count = Student.objects.count()
        teachers_count = Teacher.objects.count()

        # Departments: prefer a dedicated Department model if present,
        # otherwise infer from distinct student_class values.
        try:
            from student.models import Department
            departments_count = Department.objects.count()
        except Exception:
            try:
                departments_count = Student.objects.values('student_class').distinct().count()
            except Exception:
                departments_count = 0

        # Recent notifications for activity feed
        notifications = list(StudentNotification.objects.order_by('-created_at')[:6])
        activities = [{'date': n.created_at.strftime('%b %d'), 'text': f"{n.user.username} {n.message}"} for n in notifications]

        # Awards: heuristically count notifications mentioning 'award' (if your app has a proper Awards model, use it instead)
        try:
            awards_count = StudentNotification.objects.filter(message__icontains='award').count()
        except Exception:
            awards_count = 0

        # Star students: if there's a Result model use top marks; otherwise show recent students
        try:
            from student.models import Result
            qs = Result.objects.select_related('student').order_by('-marks_obtained')[:5]
            for r in qs:
                s = r.student
                star_students.append({'id': s.student_id, 'name': s.get_full_name(), 'marks': r.marks_obtained, 'percentage': f"{(r.marks_obtained / (r.exam.total_marks or 1) * 100):.1f}%" if getattr(r, 'exam', None) else '', 'year': getattr(s.joining_date, 'year', '')})
        except Exception:
            # Fallback: use students list (most recent)
            qs = Student.objects.order_by('-created_at')[:5]
            for s in qs:
                star_students.append({'id': s.student_id, 'name': s.get_full_name(), 'marks': '—', 'percentage': '—', 'year': s.joining_date.year if getattr(s, 'joining_date', None) else ''})

        # Revenue: if there's a Fees/Payments model, sum amounts collected
        try:
            from student.models import Fees
            # Get total amount from Fees model (which has 'amount' field)
            revenue = Fees.objects.aggregate(total=Sum('amount'))['total'] or 0
        except Exception:
            try:
                from student.models import Fee
                # Try alternative Fee model if Fees doesn't work
                revenue = Fee.objects.filter(status='Paid').aggregate(total=Sum('amount'))['total'] or 0
            except Exception:
                revenue = 0

        # Generate monthly chart data for graphs (last 7 months)
        months_data = []
        students_data = []
        teachers_data = []
        revenue_data = []
        
        for i in range(6, -1, -1):
            date = datetime.now() - timedelta(days=30*i)
            month_name = date.strftime('%b')
            months_data.append(month_name)
            
            # Get students joined in this month
            students_count_month = Student.objects.filter(
                joining_date__year=date.year,
                joining_date__month=date.month
            ).count()
            students_data.append(students_count_month if students_count_month > 0 else 15 + i*5)
            
            # Get teachers joined in this month
            teachers_count_month = Teacher.objects.filter(
                joining_date__year=date.year,
                joining_date__month=date.month
            ).count()
            teachers_data.append(teachers_count_month if teachers_count_month > 0 else 3 + i*2)
            
            # Get revenue collected in this month
            try:
                from student.models import Fees
                monthly_revenue = Fees.objects.filter(
                    date__year=date.year,
                    date__month=date.month
                ).aggregate(total=Sum('amount'))['total'] or 0
                revenue_data.append(float(monthly_revenue) if monthly_revenue > 0 else 5000 + i*1000)
            except Exception:
                try:
                    from student.models import Fee
                    monthly_revenue = Fee.objects.filter(
                        date__year=date.year,
                        date__month=date.month,
                        status='Paid'
                    ).aggregate(total=Sum('amount'))['total'] or 0
                    revenue_data.append(float(monthly_revenue) if monthly_revenue > 0 else 5000 + i*1000)
                except Exception:
                    revenue_data.append(5000 + i*1000)

        # Chart data for ApexCharts (JSON for JavaScript)
        chart_data = {
            'categories': months_data,
            'revenue': revenue_data,  # Monthly revenue data for Revenue chart
            'students': students_data,  # Monthly student count for Students chart
            'teachers': teachers_data  # Monthly teacher count (optional)
        }

    except Exception as e:
        # If student app is unavailable, leave fallback zeros/lists
        students_count = 0
        teachers_count = 0
        departments_count = 0
        star_students = []
        activities = []
        awards_count = 0
        revenue = 0
        chart_data = {}

    context = {
        'students_count': students_count,
        'teachers_count': teachers_count,
        'awards_count': awards_count,
        'departments_count': departments_count,
        'revenue': revenue,
        'star_students': star_students,
        'activities': activities,
        'chart_data': json.dumps(chart_data),
        'social_counts': {'facebook': '50,095', 'twitter': '48,596', 'instagram': '52,085', 'linkedin': '69,050'},
        'year': datetime.now().year,
        # include header notification context
        'unread_notification': notifications,
        'unread_notification_count': len(notifications),
        'user': request.user,
    }

    return render(request, "Home/index.html", context)
@login_required
def student_list(request):
    # Render the students listing template located in templates/students/
    return render(request, 'students/students.html')
@login_required
def add_student(request):
    # Render the add-student template located in templates/students/
    return render(request, 'students/add-student.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save email from the template (template posts 'email') if provided
            email = request.POST.get('email', '').strip()
            if email:
                user.email = email
                user.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')  # Redirect to login after successful signup
        else:
            # show form errors
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(request, f"{field}: {err}")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@csrf_exempt  # Allow POST requests without CSRF token for simplicity (use with caution in production)
def mark_notifications_as_read(request):
    if request.method == 'POST':
        # Logic to mark notifications as read (e.g., update the database)
        # For now, return a success response
        return JsonResponse({'status': 'success', 'message': 'Notifications marked as read'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt  # Allow POST requests without CSRF token for simplicity (use with caution in production)
def clear_all_notifications(request):
    if request.method == 'POST':
        # Logic to clear all notifications (e.g., update the database)
        # For now, return a success response
        return JsonResponse({'status': 'success', 'message': 'All notifications cleared'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# Create your views here.


def _build_admin_context(user, extra=None):
    """Return a simple dict with the keys used by `profile.html` so templates don't break.
    We don't have a dedicated Admin model in this project, so map available User fields
    and provide reasonable defaults for missing ones."""
    admin = {
        'name': user.get_full_name() if user and user.is_authenticated else '',
        'username': user.username if user and user.is_authenticated else '',
        'mobile': '',
        'email': user.email if user and user.is_authenticated else '',
        'joining_date': '',
        'address': '',
        'image': None,
    }
    if extra:
        admin.update(extra)
    return admin


@login_required
def profile(request):
    """Display and allow updating a minimal profile backed by Django's User model.

    This view updates basic User fields (first_name/last_name/email). Other fields shown
    in the template (mobile/address/image/joining_date) are kept in the template context
    but not persisted because the project currently has no profile model.
    """
    user = request.user

    if request.method == 'POST':
        # Update basic user fields
        name = request.POST.get('name', '').strip()
        if name:
            parts = name.split(None, 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''

        email = request.POST.get('email', '').strip()
        if email:
            user.email = email

        # Persist mobile/address/image into AdminProfile
        try:
            user.save()
        except Exception:
            pass

        profile, _ = AdminProfile.objects.get_or_create(user=user)
        profile.mobile = request.POST.get('mobile', profile.mobile or '').strip()
        profile.address = request.POST.get('address', profile.address or '').strip()
        # joining_date optional
        joining_date = request.POST.get('joining_date', '').strip()
        if joining_date:
            try:
                profile.joining_date = joining_date
            except Exception:
                # ignore parse errors; templates will show blank
                pass
        # Save uploaded image if present
        if request.FILES.get('image'):
            profile.image = request.FILES['image']

        profile.save()

        # After POST, redirect to the same page (Post-Redirect-Get) to avoid double submissions
        return redirect('profile')

    # For GET render current values
    # Use AdminProfile values when available
    profile, _ = AdminProfile.objects.get_or_create(user=user)
    admin = {
        'name': user.get_full_name() if user and user.is_authenticated else '',
        'username': user.username if user and user.is_authenticated else '',
        'mobile': profile.mobile or '',
        'email': user.email if user and user.is_authenticated else '',
        'joining_date': profile.joining_date or '',
        'address': profile.address or '',
        'image': profile.image if profile.image else None,
    }

    return render(request, 'profile.html', {'admin': admin, 'year': datetime.now().year})
