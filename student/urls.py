from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Authentication - redirect to central auth routes to avoid conflicts
    path('login/', RedirectView.as_view(url='/login/'), name='student_login_redirect'),
    path('signup/', RedirectView.as_view(url='/signup/'), name='student_signup_redirect'),
    path('logout/', RedirectView.as_view(url='/logout/'), name='student_logout_redirect'),
    path('forgot-password/', RedirectView.as_view(url='/forgot-password/'), name='student_forgot_password_redirect'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<slug:slug>/', views.view_student, name='view_student'),
    path('students/<slug:slug>/edit/', views.edit_student, name='edit_student'),
    path('students/<slug:slug>/delete/', views.delete_student, name='delete_student'),
    
    # Notifications
    path('notifications/mark-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('notifications/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),

    # Additional placeholder pages (teachers, departments, subjects, fees, etc.)
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/add/', views.add_teacher, name='add_teacher_page'),
    path('teachers/<slug:slug>/edit/', views.edit_teacher, name='edit_teacher_page'),
    path('teachers/<slug:slug>/delete/', views.delete_teacher, name='delete_teacher'),
    path('teachers/<slug:slug>/', views.teacher_details, name='teacher_details'),

    path('departments/', views.departments_view, name='departments'),
    path('departments/add/', views.add_department_view, name='add_department'),
    path('departments/<int:id>/edit/', views.edit_department_view, name='edit_department'),
    path('departments/<int:id>/delete/', views.delete_department_view, name='delete_department'),

    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/add/', views.add_subject_view, name='add_subject'),
    path('subjects/<int:id>/edit/', views.edit_subject_view, name='edit_subject'),
    path('subjects/<int:id>/delete/', views.delete_subject_view, name='delete_subject'),

    path('fees-collections/', views.fees_collections_view, name='fees_collections'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('salary/', views.salary_view, name='salary'),
    path('fees-collections/add/', views.add_fees_collection_view, name='add_fees_collection'),
    path('fees-collections/edit/<int:id>/', views.edit_fees_collection_view, name='edit_fees'),
    path('expenses/add/', views.add_expenses_view, name='add_expenses'),
    path('expenses/edit/<int:id>/', views.edit_expense_view, name='edit_expense'),
    path('expenses/delete/<int:id>/', views.delete_expense_view, name='delete_expense'),
    path('salary/add/', views.add_salary_view, name='add_salary'),
    path('salary/<int:id>/edit/', views.edit_salary_view, name='edit_salary'),
    path('salary/<int:id>/delete/', views.delete_salary_view, name='delete_salary'),

    path('holiday/', views.holiday, name='holiday'),
    path('add/holiday/', views.holiday_add, name='add_holiday'),
    path('holiday/edit/<int:id>/', views.edit_holiday, name='edit_holiday'),
    path('holiday/delete/<int:id>/', views.delete_holiday, name='delete_holiday'),

    # path('fees/', views.fees_view, name='fees'),
    # path('add/fees/', views.fees_add, name='fees_add'),
    # path('exam/', views.exam_view, name='exam'),
    # path('event/', views.event_view, name='event'),
    path('time-table/', views.time_table_view, name='time_table'),
    # path('library/', views.library_view, name='library'),

    # path('sports/', views.sports_view, name='sports'),
    # path('hostel/', views.hostel_view, name='hostel'),
    path('transport/', views.transport_view, name='transport'),
   
    path('fees/', views.fees_list, name='fees'),
    path('fees/add/', views.add_fees, name='add_fees'),
    path('fees/edit/<int:id>/', views.edit_fees, name='edit_fees'),
    path('fees/delete/<int:id>/', views.delete_fees, name='delete_fees'),  # New
    path('exam/', views.exam_list, name='exam'),
    path('exam/add/', views.add_exam, name='add_exam'),
    path('exam/edit/<int:id>/', views.edit_exam, name='edit_exam'),
    path('exam/delete/<int:id>/', views.delete_exam, name='delete_exam'),


    path('event/', views.event_list, name='event_list'),
    path('search/', views.search, name='search'),
    path('event/add/', views.add_event, name='add_event'),
    path('event/edit/<int:id>/', views.edit_event, name='edit_event'),
    path('event/delete/<int:id>/', views.delete_event, name='delete_event'),


    # Timetable routes (add/edit/delete). Using the existing `time-table/` prefix.
    path('time-table/add/', views.add_timetable, name='add_timetable'),
    path('time-table/edit/<int:id>/', views.edit_timetable, name='edit_timetable'),
    path('time-table/delete/<int:id>/', views.delete_timetable, name='delete_timetable'),


    path('library/', views.library, name="library"),
    path('delete-book/<int:id>/', views.delete_book, name="delete_book"),

    path('sports/', views.sports, name="sports"),
    path('delete-sport/<int:id>/', views.delete_sport, name="delete_sport"),

    path('hostel/', views.hostel, name="hostel"),
    path('delete-hostel/<int:id>/', views.delete_hostel, name="delete_hostel"),


]