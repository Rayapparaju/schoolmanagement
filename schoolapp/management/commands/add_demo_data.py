from datetime import date, timedelta
from decimal import Decimal
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from schoolapp.models import Teacher, Class, Subject, Student, Attendance, Fee, Exam, Notice


class Command(BaseCommand):
    help = 'Add demo data for testing the School Management System'

    def handle(self, *args, **options):
        self.stdout.write('Adding demo data...')

        # ─── Teachers ───
        teachers_data = [
            {'first_name': 'Rajesh', 'last_name': 'Kumar', 'phone': '9876543210', 'email': 'rajesh.kumar@school.com', 'address': '12 MG Road, Mumbai', 'joining_date': date(2022, 6, 1)},
            {'first_name': 'Priya', 'last_name': 'Sharma', 'phone': '9876543211', 'email': 'priya.sharma@school.com', 'address': '45 Lokhandwala, Mumbai', 'joining_date': date(2021, 8, 15)},
            {'first_name': 'Amit', 'last_name': 'Singh', 'phone': '9876543212', 'email': 'amit.singh@school.com', 'address': '78 Model Town, Delhi', 'joining_date': date(2023, 1, 10)},
            {'first_name': 'Sunita', 'last_name': 'Patel', 'phone': '9876543213', 'email': 'sunita.patel@school.com', 'address': '34 Satellite Road, Ahmedabad', 'joining_date': date(2022, 11, 20)},
            {'first_name': 'Vikram', 'last_name': 'Mehta', 'phone': '9876543214', 'email': 'vikram.mehta@school.com', 'address': '56 Koramangala, Bangalore', 'joining_date': date(2023, 4, 5)},
        ]
        teachers = []
        for t in teachers_data:
            teacher, created = Teacher.objects.get_or_create(email=t['email'], defaults=t)
            teachers.append(teacher)
            if created:
                self.stdout.write(f'  Created teacher: {teacher}')

        # ─── Classes ───
        classes_data = [
            {'name': 'Class 1', 'section': 'A', 'class_teacher': teachers[0]},
            {'name': 'Class 1', 'section': 'B', 'class_teacher': teachers[1]},
            {'name': 'Class 2', 'section': 'A', 'class_teacher': teachers[2]},
            {'name': 'Class 2', 'section': 'B', 'class_teacher': teachers[3]},
            {'name': 'Class 3', 'section': 'A', 'class_teacher': teachers[4]},
            {'name': 'Class 3', 'section': 'B', 'class_teacher': teachers[0]},
            {'name': 'Class 4', 'section': 'A', 'class_teacher': teachers[1]},
            {'name': 'Class 4', 'section': 'B', 'class_teacher': teachers[2]},
        ]
        classes = []
        for c in classes_data:
            cls, created = Class.objects.get_or_create(name=c['name'], section=c['section'], defaults={'class_teacher': c['class_teacher']})
            classes.append(cls)
            if created:
                self.stdout.write(f'  Created class: {cls}')

        # ─── Subjects ───
        subject_names = ['Mathematics', 'Science', 'English', 'Hindi', 'Computer Science']
        teacher_idx = 0
        subjects = []
        for cls in classes:
            for i, sub_name in enumerate(subject_names):
                teacher = teachers[teacher_idx % len(teachers)]
                teacher_idx += 1
                sub, created = Subject.objects.get_or_create(name=sub_name, student_class=cls, defaults={'teacher': teacher})
                subjects.append(sub)
                if created:
                    self.stdout.write(f'  Created subject: {sub}')

        # ─── Students ───
        students_data = [
            {'admission_number': 'STU001', 'first_name': 'Aarav', 'last_name': 'Verma', 'gender': 'Male', 'date_of_birth': date(2014, 5, 12), 'parent_name': 'Ravi Verma', 'parent_phone': '9988776651', 'address': '12 Sector 15, Noida', 'phone': '9988776651', 'email': 'aarav.verma@example.com'},
            {'admission_number': 'STU002', 'first_name': 'Ananya', 'last_name': 'Gupta', 'gender': 'Female', 'date_of_birth': date(2015, 8, 25), 'parent_name': 'Neha Gupta', 'parent_phone': '9988776652', 'address': '34 Sector 12, Noida', 'phone': '9988776652', 'email': 'ananya.gupta@example.com'},
            {'admission_number': 'STU003', 'first_name': 'Rohan', 'last_name': 'Joshi', 'gender': 'Male', 'date_of_birth': date(2013, 2, 18), 'parent_name': 'Prakash Joshi', 'parent_phone': '9988776653', 'address': '56 Gandhi Nagar, Delhi', 'phone': '9988776653', 'email': 'rohan.joshi@example.com'},
            {'admission_number': 'STU004', 'first_name': 'Ishita', 'last_name': 'Reddy', 'gender': 'Female', 'date_of_birth': date(2014, 11, 5), 'parent_name': 'Suresh Reddy', 'parent_phone': '9988776654', 'address': '78 Jubilee Hills, Hyderabad', 'phone': '9988776654', 'email': 'ishita.reddy@example.com'},
            {'admission_number': 'STU005', 'first_name': 'Arjun', 'last_name': 'Nair', 'gender': 'Male', 'date_of_birth': date(2015, 7, 30), 'parent_name': 'Deepa Nair', 'parent_phone': '9988776655', 'address': '90 Marine Drive, Kochi', 'phone': '9988776655', 'email': 'arjun.nair@example.com'},
            {'admission_number': 'STU006', 'first_name': 'Kavya', 'last_name': 'Patil', 'gender': 'Female', 'date_of_birth': date(2013, 4, 15), 'parent_name': 'Anita Patil', 'parent_phone': '9988776656', 'address': '23 FC Road, Pune', 'phone': '9988776656', 'email': 'kavya.patil@example.com'},
            {'admission_number': 'STU007', 'first_name': 'Vivaan', 'last_name': 'Saxena', 'gender': 'Male', 'date_of_birth': date(2014, 9, 8), 'parent_name': 'Raj Saxena', 'parent_phone': '9988776657', 'address': '67 Civil Lines, Lucknow', 'phone': '9988776657', 'email': 'vivaan.saxena@example.com'},
            {'admission_number': 'STU008', 'first_name': 'Myra', 'last_name': 'Das', 'gender': 'Female', 'date_of_birth': date(2015, 1, 22), 'parent_name': 'Mita Das', 'parent_phone': '9988776658', 'address': '45 Salt Lake, Kolkata', 'phone': '9988776658', 'email': 'myra.das@example.com'},
            {'admission_number': 'STU009', 'first_name': 'Aditya', 'last_name': 'Chauhan', 'gender': 'Male', 'date_of_birth': date(2013, 6, 14), 'parent_name': 'Vikram Chauhan', 'parent_phone': '9988776659', 'address': '89 Bapunagar, Jaipur', 'phone': '9988776659', 'email': 'aditya.chauhan@example.com'},
            {'admission_number': 'STU010', 'first_name': 'Sara', 'last_name': 'Khan', 'gender': 'Female', 'date_of_birth': date(2014, 12, 3), 'parent_name': 'Imran Khan', 'parent_phone': '9988776660', 'address': '12 Bandra West, Mumbai', 'phone': '9988776660', 'email': 'sara.khan@example.com'},
            {'admission_number': 'STU011', 'first_name': 'Reyansh', 'last_name': 'Tiwari', 'gender': 'Male', 'date_of_birth': date(2015, 3, 27), 'parent_name': 'Shalini Tiwari', 'parent_phone': '9988776661', 'address': '56 Bhelupur, Varanasi', 'phone': '9988776661', 'email': 'reyansh.tiwari@example.com'},
            {'admission_number': 'STU012', 'first_name': 'Aanya', 'last_name': 'Menon', 'gender': 'Female', 'date_of_birth': date(2013, 10, 19), 'parent_name': 'Gopal Menon', 'parent_phone': '9988776662', 'address': '34 Panjagutta, Chennai', 'phone': '9988776662', 'email': 'aanya.menon@example.com'},
        ]
        students = []
        for i, s in enumerate(students_data):
            cls = classes[i % len(classes)]
            student, created = Student.objects.get_or_create(admission_number=s['admission_number'], defaults={**s, 'student_class': cls})
            students.append(student)
            if created:
                self.stdout.write(f'  Created student: {student}')

        # ─── Attendance (last 15 days) ───
        today = date.today()
        for student in students:
            for day_offset in range(15):
                d = today - timedelta(days=day_offset)
                if d.weekday() >= 5:
                    continue
                status = 'Present' if random.random() > 0.15 else 'Absent'
                _, created = Attendance.objects.get_or_create(student=student, date=d, defaults={'status': status})

        self.stdout.write(f'  Added attendance records')

        # ─── Fees ───
        fee_configs = [
            (30000, 30000), (25000, 15000), (28000, 0), (32000, 32000),
            (26000, 26000), (30000, 18000), (27000, 0), (29000, 29000),
            (31000, 10000), (28000, 28000), (25000, 0), (33000, 33000),
        ]
        for i, student in enumerate(students):
            total, paid = fee_configs[i % len(fee_configs)]
            payment_date = today - timedelta(days=random.randint(10, 60)) if paid > 0 else None
            fee, created = Fee.objects.get_or_create(
                student=student,
                total_amount=Decimal(str(total)),
                paid_amount=Decimal(str(paid)),
                payment_date=payment_date,
            )
        self.stdout.write(f'  Added {len(students)} fee records')

        # ─── Exams ───
        exam_names = ['Mid Term 2025', 'Quarterly 2025', 'Half Yearly 2025']
        for student in students:
            student_subjects = Subject.objects.filter(student_class=student.student_class)
            for exam_name in exam_names[:2]:
                for subject in student_subjects:
                    marks = Decimal(str(round(random.uniform(35, 98), 2)))
                    exam, created = Exam.objects.get_or_create(
                        name=exam_name,
                        student=student,
                        subject=subject,
                        defaults={'marks': marks},
                    )
        self.stdout.write(f'  Added exam records for {len(students)} students')

        # ─── Notices ───
        notices_data = [
            {'title': 'School Reopening After Holidays', 'content': 'The school will reopen on Monday, 5th January 2026. All students are expected to report to their respective classes by 8:00 AM. Please ensure that all homework and assignments are completed and submitted on the first day.'},
            {'title': 'Parent-Teacher Meeting Scheduled', 'content': 'The annual parent-teacher meeting has been scheduled for Saturday, 15th February 2026 from 9:00 AM to 2:00 PM. All parents are requested to attend and meet with the respective subject teachers to discuss student progress.'},
            {'title': 'Annual Sports Day 2026', 'content': 'The Annual Sports Day will be held on 28th February 2026 at the school grounds. Students interested in participating must register with their class teacher by 10th February. Events include athletics, team sports, and fun games.'},
            {'title': 'Summer Vacation Notice', 'content': 'Summer vacation will commence from 1st May 2026 to 15th June 2026. The school will reopen on 16th June 2026. Summer project assignments have been uploaded to the student portal. Please complete and submit them by the reopening date.'},
        ]
        for i, n in enumerate(notices_data):
            notice, created = Notice.objects.get_or_create(title=n['title'], defaults={'content': n['content'], 'is_active': True})
            if created:
                self.stdout.write(f'  Created notice: {notice.title}')

        self.stdout.write(self.style.SUCCESS(f'Successfully added demo data: {len(teachers)} teachers, {len(classes)} classes, {len(students)} students, exams, fees, attendance, and notices.'))
