import csv
from django.core.management.base import BaseCommand
from schoolapp.models import Student, Teacher, Class, Subject, Fee


class Command(BaseCommand):
    help = 'Import data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model name: Student, Teacher, Subject, Fee')
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        model_name = options['model']
        file_path = options['csv_file']
        imported = 0
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        if model_name == 'Student':
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
                        elif model_name == 'Teacher':
                            Teacher.objects.create(
                                first_name=row.get('first_name', ''),
                                last_name=row.get('last_name', ''),
                                phone=row.get('phone', ''),
                                email=row.get('email', ''),
                                address=row.get('address', ''),
                                joining_date=row.get('joining_date', '2024-01-01'),
                            )
                        elif model_name == 'Fee':
                            student = Student.objects.filter(admission_number=row.get('admission_number')).first()
                            if student:
                                Fee.objects.create(
                                    student=student,
                                    total_amount=row.get('total_amount', 0),
                                    paid_amount=row.get('paid_amount', 0),
                                    payment_date=row.get('payment_date', None) or None,
                                )
                        elif model_name == 'Subject':
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

            self.stdout.write(self.style.SUCCESS(f"Imported {imported} records."))
            if errors:
                for e in errors:
                    self.stdout.write(self.style.ERROR(e))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
