from django.contrib import admin
from .models import Student, Teacher, Class, Subject, Attendance, Fee, Exam, Notice


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'first_name', 'last_name', 'gender', 'student_class', 'phone', 'email']
    list_filter = ['gender', 'student_class']
    search_fields = ['first_name', 'last_name', 'admission_number', 'email']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'joining_date']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'class_teacher']
    list_filter = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_class', 'teacher']
    list_filter = ['student_class']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status']
    list_filter = ['date', 'status']
    search_fields = ['student__first_name', 'student__last_name']


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'total_amount', 'paid_amount', 'due_amount', 'status', 'payment_date']
    list_filter = ['status']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'student', 'subject', 'marks', 'grade', 'result_status']
    list_filter = ['name', 'result_status']


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']
