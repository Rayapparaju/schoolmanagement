import csv
import io
import os
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .whatsapp_utils import generate_wa_link, send_via_twilio
from .models import Student, Teacher, Class, Subject, Attendance, Fee, Exam, Notice
from .forms import StudentForm, TeacherForm, ClassForm, SubjectForm, AttendanceForm, FeeForm, ExamForm, NoticeForm, ImportCSVForm


def home(request):
    notices = Notice.objects.filter(is_active=True)[:5]
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    class_count = Class.objects.count()
    context = {
        'notices': notices,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'class_count': class_count,
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_home(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()
    total_subjects = Subject.objects.count()
    total_fees = Fee.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    pending_fees = Fee.objects.filter(status='Unpaid').count()
    recent_admissions = Student.objects.order_by('-created_at')[:5]
    recent_fees = Fee.objects.order_by('-created_at')[:5]
    class_distribution = Student.objects.values('student_class__name').annotate(count=Count('id'))
    gender_distribution = Student.objects.values('gender').annotate(count=Count('id'))
    attendance_data = Attendance.objects.values('status').annotate(count=Count('id'))

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'total_fees': total_fees,
        'pending_fees': pending_fees,
        'recent_admissions': recent_admissions,
        'recent_fees': recent_fees,
        'class_distribution': list(class_distribution),
        'gender_distribution': list(gender_distribution),
        'attendance_data': list(attendance_data),
    }
    return render(request, 'dashboard/home.html', context)


# ─── Students ───
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'dashboard/students/list.html', {'students': students})


@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'dashboard/students/add.html', {'form': form})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'dashboard/students/edit.html', {'form': form, 'student': student})


@login_required
def student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    fees = Fee.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student).order_by('-date')[:20]
    exams = Exam.objects.filter(student=student)
    return render(request, 'dashboard/students/view.html', {
        'student': student,
        'fees': fees,
        'attendance': attendance,
        'exams': exams,
    })


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('student_list')


# ─── Teachers ───
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'dashboard/teachers/list.html', {'teachers': teachers})


@login_required
def teacher_add(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'dashboard/teachers/add.html', {'form': form})


@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'dashboard/teachers/edit.html', {'form': form, 'teacher': teacher})


@login_required
def teacher_view(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'dashboard/teachers/view.html', {'teacher': teacher})


@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully.')
    return redirect('teacher_list')


# ─── Classes ───
@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'dashboard/classes/list.html', {'classes': classes})


@login_required
def class_add(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class added successfully.')
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'dashboard/classes/add.html', {'form': form})


@login_required
def class_edit(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully.')
            return redirect('class_list')
    else:
        form = ClassForm(instance=cls)
    return render(request, 'dashboard/classes/edit.html', {'form': form, 'class': cls})


@login_required
def class_delete(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    cls.delete()
    messages.success(request, 'Class deleted successfully.')
    return redirect('class_list')


# ─── Subjects ───
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'dashboard/subjects/list.html', {'subjects': subjects})


@login_required
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'dashboard/subjects/add.html', {'form': form})


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'dashboard/subjects/edit.html', {'form': form, 'subject': subject})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, 'Subject deleted successfully.')
    return redirect('subject_list')


# ─── Attendance ───
@login_required
def attendance_list(request):
    records = Attendance.objects.all().order_by('-date')
    return render(request, 'dashboard/attendance/list.html', {'records': records})


@login_required
def attendance_add(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'dashboard/attendance/add.html', {'form': form})


@login_required
def attendance_delete(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    record.delete()
    messages.success(request, 'Attendance record deleted.')
    return redirect('attendance_list')


# ─── Fees ───
@login_required
def fee_list(request):
    fees = Fee.objects.all()
    student_id = request.GET.get('student')
    status_filter = request.GET.get('status')
    if student_id:
        fees = fees.filter(student_id=student_id)
    if status_filter:
        fees = fees.filter(status=status_filter)
    total_collected = fees.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_due = fees.aggregate(Sum('due_amount'))['due_amount__sum'] or 0
    students = Student.objects.all().order_by('first_name')
    return render(request, 'dashboard/fees/list.html', {
        'fees': fees,
        'total_collected': total_collected,
        'total_due': total_due,
        'students': students,
        'selected_student': student_id,
        'selected_status': status_filter,
    })


@login_required
def fee_add(request):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record added successfully.')
            return redirect('fee_list')
    else:
        form = FeeForm()
    return render(request, 'dashboard/fees/add.html', {'form': form})


@login_required
def fee_edit(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record updated successfully.')
            return redirect('fee_list')
    else:
        form = FeeForm(instance=fee)
    return render(request, 'dashboard/fees/edit.html', {'form': form, 'fee': fee})


@login_required
def fee_delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    fee.delete()
    messages.success(request, 'Fee record deleted.')
    return redirect('fee_list')


@login_required
def student_fee_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    fees = Fee.objects.filter(student=student).order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        fees = fees.filter(status=status_filter)
    total_paid = fees.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_due = fees.aggregate(Sum('due_amount'))['due_amount__sum'] or 0
    context = {
        'student': student,
        'fees': fees,
        'total_paid': total_paid,
        'total_due': total_due,
        'selected_status': status_filter,
    }
    return render(request, 'dashboard/fees/student_detail.html', context)


@login_required
def student_fee_pdf(request, pk):
    from django.template.loader import render_to_string
    from xhtml2pdf import pisa
    from io import BytesIO

    student = get_object_or_404(Student, pk=pk)
    fees = Fee.objects.filter(student=student).order_by('-created_at')
    total_paid = fees.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_due = fees.aggregate(Sum('due_amount'))['due_amount__sum'] or 0

    html = render_to_string('dashboard/fees/fee_pdf.html', {
        'student': student,
        'fees': fees,
        'total_paid': total_paid,
        'total_due': total_due,
    })

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if pdf.err:
        return HttpResponse('PDF generation error', status=500)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.admission_number}_fees.pdf"'
    return response


# ─── Exams ───
@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'dashboard/exams/list.html', {'exams': exams})


@login_required
def exam_add(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam result added successfully.')
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'dashboard/exams/add.html', {'form': form})


@login_required
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam result updated successfully.')
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'dashboard/exams/edit.html', {'form': form, 'exam': exam})


@login_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.delete()
    messages.success(request, 'Exam record deleted.')
    return redirect('exam_list')


# ─── Notices ───
@login_required
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'dashboard/notices/list.html', {'notices': notices})


@login_required
def notice_add(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice created successfully.')
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'dashboard/notices/add.html', {'form': form})


@login_required
def notice_edit(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully.')
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'dashboard/notices/edit.html', {'form': form, 'notice': notice})


@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    messages.success(request, 'Notice deleted.')
    return redirect('notice_list')


# ─── Import Data ───
@login_required
def import_data(request):
    if request.method == 'POST':
        form = ImportCSVForm(request.POST, request.FILES)
        if form.is_valid():
            model_choice = form.cleaned_data['model_choice']
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            imported = 0
            errors = []

            try:
                for row in reader:
                    try:
                        if model_choice == 'Student':
                            class_obj = None
                            if row.get('student_class'):
                                class_obj = Class.objects.filter(name=row['student_class']).first()
                            Student.objects.create(
                                admission_number=row.get('admission_number', ''),
                                first_name=row.get('first_name', ''),
                                last_name=row.get('last_name', ''),
                                gender=row.get('gender', 'Male'),
                                date_of_birth=row.get('date_of_birth', '2000-01-01'),
                                student_class=class_obj,
                                parent_name=row.get('parent_name', ''),
                                parent_phone=row.get('parent_phone', ''),
                                address=row.get('address', ''),
                                phone=row.get('phone', ''),
                                email=row.get('email', ''),
                            )
                        elif model_choice == 'Teacher':
                            Teacher.objects.create(
                                first_name=row.get('first_name', ''),
                                last_name=row.get('last_name', ''),
                                phone=row.get('phone', ''),
                                email=row.get('email', ''),
                                address=row.get('address', ''),
                                joining_date=row.get('joining_date', '2024-01-01'),
                            )
                        elif model_choice == 'Fee':
                            student = Student.objects.filter(admission_number=row.get('admission_number')).first()
                            if student:
                                Fee.objects.create(
                                    student=student,
                                    total_amount=row.get('total_amount', 0),
                                    paid_amount=row.get('paid_amount', 0),
                                    payment_date=row.get('payment_date', None) or None,
                                )
                        elif model_choice == 'Subject':
                            class_obj = None
                            teacher = None
                            if row.get('class_name'):
                                class_obj = Class.objects.filter(name=row['class_name']).first()
                            if row.get('teacher_email'):
                                teacher = Teacher.objects.filter(email=row['teacher_email']).first()
                            Subject.objects.create(
                                name=row.get('name', ''),
                                student_class=class_obj,
                                teacher=teacher,
                            )
                        imported += 1
                    except Exception as e:
                        errors.append(f"Row {imported + 2}: {str(e)}")

                if errors:
                    messages.warning(request, f"Imported {imported} records with {len(errors)} errors.")
                else:
                    messages.success(request, f"Successfully imported {imported} records.")
            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
            return redirect('import_data')
    else:
        form = ImportCSVForm()
    return render(request, 'dashboard/import_data.html', {'form': form})


@login_required
def download_sample_csv(request, model_name):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}_sample.csv"'

    writer = csv.writer(response)
    if model_name == 'Student':
        writer.writerow(['admission_number', 'first_name', 'last_name', 'gender', 'date_of_birth', 'student_class', 'parent_name', 'parent_phone', 'address', 'phone', 'email'])
        writer.writerow(['S001', 'John', 'Doe', 'Male', '2010-05-15', 'Class 5', 'Jane Doe', '+1234567890', '123 Main St', '+123456789', 'john@example.com'])
    elif model_name == 'Teacher':
        writer.writerow(['first_name', 'last_name', 'phone', 'email', 'address', 'joining_date'])
        writer.writerow(['Alice', 'Smith', '+1234567890', 'alice@school.com', '456 Oak Ave', '2023-08-01'])
    elif model_name == 'Fee':
        writer.writerow(['admission_number', 'total_amount', 'paid_amount', 'payment_date'])
        writer.writerow(['S001', '5000', '5000', '2024-01-15'])
    elif model_name == 'Subject':
        writer.writerow(['name', 'class_name', 'teacher_email'])
        writer.writerow(['Mathematics', 'Class 5', 'alice@school.com'])
    return response


# ─── WhatsApp Notifications ───

def _build_attendance_msg(student, records):
    present = records.filter(status='Present').count()
    absent = records.filter(status='Absent').count()
    total = records.count()
    lines = [
        f'*📋 Attendance Report – {student.first_name} {student.last_name}*',
        f'*Admission:* {student.admission_number}',
        f'*Class:* {student.student_class}',
        f'',
        f'Total records: {total}',
        f'✅ Present: {present}',
        f'❌ Absent: {absent}',
        f'Attendance %: {present/total*100:.0f}%' if total else 'N/A',
        f'',
        f'── Last 5 Records ──',
    ]
    for r in records.order_by('-date')[:5]:
        lines.append(f'{r.date} → {"✅" if r.status == "Present" else "❌"} {r.status}')
    lines.append('')
    lines.append('_School Management System_')
    return '\n'.join(lines)


def _build_fee_msg(student, fees):
    total_amt = sum(f.total_amount for f in fees)
    paid_amt = sum(f.paid_amount for f in fees)
    due_amt = total_amt - paid_amt
    lines = [
        f'*💰 Fee Statement – {student.first_name} {student.last_name}*',
        f'*Admission:* {student.admission_number}',
        f'*Class:* {student.student_class}',
        f'',
        f'*Total Fees:* ₹{total_amt:,.2f}',
        f'*Paid:* ₹{paid_amt:,.2f}',
        f'*Due:* ₹{due_amt:,.2f}',
        f'',
        f'── Fee Records ──',
    ]
    for f in fees:
        lines.append(f'₹{f.total_amount:,.0f} | Paid: ₹{f.paid_amount:,.0f} | Due: ₹{f.due_amount:,.0f} | {f.status}')
    lines.append('')
    lines.append('_School Management System_')
    return '\n'.join(lines)


def _build_exam_msg(student, exams):
    lines = [
        f'*📝 Exam Results – {student.first_name} {student.last_name}*',
        f'*Admission:* {student.admission_number}',
        f'*Class:* {student.student_class}',
        f'',
        f'── Results ──',
    ]
    for e in exams:
        lines.append(f'{e.name} | {e.subject.name} | Marks: {e.marks} | Grade: {e.grade} | {e.result_status}')
    lines.append('')
    lines.append('_School Management System_')
    return '\n'.join(lines)


@login_required
def send_attendance_whatsapp(request, pk):
    student = get_object_or_404(Student, pk=pk)
    records = Attendance.objects.filter(student=student)
    if not records.exists():
        messages.warning(request, 'No attendance records to send.')
        return redirect('attendance_list')

    phone = student.parent_phone
    msg = _build_attendance_msg(student, records)

    if request.GET.get('mode') == 'api' and settings.TWILIO_ACCOUNT_SID:
        ok = send_via_twilio(phone, msg)
        if ok:
            messages.success(request, f'Attendance sent via WhatsApp to {student.parent_name}.')
        else:
            messages.error(request, 'Failed to send via WhatsApp API.')
        return redirect('attendance_list')

    wa_link = generate_wa_link(phone, msg)
    return redirect(wa_link)


@login_required
def send_fee_whatsapp(request, pk):
    student = get_object_or_404(Student, pk=pk)
    fees = Fee.objects.filter(student=student)
    if not fees.exists():
        messages.warning(request, 'No fee records to send.')
        return redirect('fee_list')

    phone = student.parent_phone
    msg = _build_fee_msg(student, fees)

    if request.GET.get('mode') == 'api' and settings.TWILIO_ACCOUNT_SID:
        ok = send_via_twilio(phone, msg)
        if ok:
            messages.success(request, f'Fee statement sent via WhatsApp to {student.parent_name}.')
        else:
            messages.error(request, 'Failed to send via WhatsApp API.')
        return redirect('fee_list')

    wa_link = generate_wa_link(phone, msg)
    return redirect(wa_link)


@login_required
def send_exam_whatsapp(request, pk):
    student = get_object_or_404(Student, pk=pk)
    exams = Exam.objects.filter(student=student)
    if not exams.exists():
        messages.warning(request, 'No exam records to send.')
        return redirect('exam_list')

    phone = student.parent_phone
    msg = _build_exam_msg(student, exams)

    if request.GET.get('mode') == 'api' and settings.TWILIO_ACCOUNT_SID:
        ok = send_via_twilio(phone, msg)
        if ok:
            messages.success(request, f'Exam results sent via WhatsApp to {student.parent_name}.')
        else:
            messages.error(request, 'Failed to send via WhatsApp API.')
        return redirect('exam_list')

    wa_link = generate_wa_link(phone, msg)
    return redirect(wa_link)
