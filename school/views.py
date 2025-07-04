from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,"Home/index.html")

def student_list(request):
    return render(request, 'student_list.html')  # Ensure the template exists

def add_student(request):
    return render(request, 'add_student.html')  # Ensure the template exists

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful signup
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
