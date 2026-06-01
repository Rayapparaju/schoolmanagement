from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_home, name='dashboard_home'),

    # Students
    path('dashboard/students/', views.student_list, name='student_list'),
    path('dashboard/students/add/', views.student_add, name='student_add'),
    path('dashboard/students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('dashboard/students/<int:pk>/view/', views.student_view, name='student_view'),
    path('dashboard/students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Teachers
    path('dashboard/teachers/', views.teacher_list, name='teacher_list'),
    path('dashboard/teachers/add/', views.teacher_add, name='teacher_add'),
    path('dashboard/teachers/<int:pk>/edit/', views.teacher_edit, name='teacher_edit'),
    path('dashboard/teachers/<int:pk>/view/', views.teacher_view, name='teacher_view'),
    path('dashboard/teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    # Classes
    path('dashboard/classes/', views.class_list, name='class_list'),
    path('dashboard/classes/add/', views.class_add, name='class_add'),
    path('dashboard/classes/<int:pk>/edit/', views.class_edit, name='class_edit'),
    path('dashboard/classes/<int:pk>/delete/', views.class_delete, name='class_delete'),

    # Subjects
    path('dashboard/subjects/', views.subject_list, name='subject_list'),
    path('dashboard/subjects/add/', views.subject_add, name='subject_add'),
    path('dashboard/subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('dashboard/subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    # Attendance
    path('dashboard/attendance/', views.attendance_list, name='attendance_list'),
    path('dashboard/attendance/add/', views.attendance_add, name='attendance_add'),
    path('dashboard/attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),

    # Fees
    path('dashboard/fees/', views.fee_list, name='fee_list'),
    path('dashboard/fees/add/', views.fee_add, name='fee_add'),
    path('dashboard/fees/<int:pk>/edit/', views.fee_edit, name='fee_edit'),
    path('dashboard/fees/<int:pk>/delete/', views.fee_delete, name='fee_delete'),
    path('dashboard/fees/student/<int:pk>/', views.student_fee_detail, name='student_fee_detail'),
    path('dashboard/fees/student/<int:pk>/pdf/', views.student_fee_pdf, name='student_fee_pdf'),

    # Exams
    path('dashboard/exams/', views.exam_list, name='exam_list'),
    path('dashboard/exams/add/', views.exam_add, name='exam_add'),
    path('dashboard/exams/<int:pk>/edit/', views.exam_edit, name='exam_edit'),
    path('dashboard/exams/<int:pk>/delete/', views.exam_delete, name='exam_delete'),

    # Notices
    path('dashboard/notices/', views.notice_list, name='notice_list'),
    path('dashboard/notices/add/', views.notice_add, name='notice_add'),
    path('dashboard/notices/<int:pk>/edit/', views.notice_edit, name='notice_edit'),
    path('dashboard/notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),

    # Import
    path('dashboard/import/', views.import_data, name='import_data'),
    path('dashboard/import/sample/<str:model_name>/', views.download_sample_csv, name='download_sample_csv'),

    # WhatsApp
    path('whatsapp/attendance/<int:pk>/', views.send_attendance_whatsapp, name='send_attendance_whatsapp'),
    path('whatsapp/fee/<int:pk>/', views.send_fee_whatsapp, name='send_fee_whatsapp'),
    path('whatsapp/exam/<int:pk>/', views.send_exam_whatsapp, name='send_exam_whatsapp'),
]
