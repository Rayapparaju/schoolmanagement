from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Class(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=20)
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='classes')

    class Meta:
        verbose_name_plural = 'Classes'
        unique_together = ('name', 'section')

    def __str__(self):
        return f"{self.name} - {self.section}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    joining_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.student_class})"


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    admission_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    parent_name = models.CharField(max_length=200)
    parent_phone = models.CharField(max_length=20)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Partial', 'Partial'),
        ('Unpaid', 'Unpaid'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.due_amount = self.total_amount - self.paid_amount
        if self.due_amount <= 0:
            self.status = 'Paid'
        elif self.paid_amount > 0:
            self.status = 'Partial'
        else:
            self.status = 'Unpaid'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - Fee ₹{self.total_amount}"


class Exam(models.Model):
    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('Award', 'Award'),
    ]
    name = models.CharField(max_length=200)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=2, blank=True)
    result_status = models.CharField(max_length=10, choices=RESULT_CHOICES, default='Pass')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.marks >= 90:
            self.grade = 'A+'
        elif self.marks >= 80:
            self.grade = 'A'
        elif self.marks >= 70:
            self.grade = 'B'
        elif self.marks >= 60:
            self.grade = 'C'
        elif self.marks >= 50:
            self.grade = 'D'
        else:
            self.grade = 'F'
            self.result_status = 'Fail'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.student} - {self.subject}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
