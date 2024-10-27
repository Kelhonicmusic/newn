from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    # Add fields as needed

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    # Add  fields as needed

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course_type = models.CharField(max_length=50)  # Define choices if necessary
    lessons_count = models.IntegerField()
    materials = models.TextField()  # This should remain a TextField for storing descriptions
    teacher = models.ForeignKey(Teacher, related_name='courses', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    lesson_number = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.DurationField()  # Time duration for the lesson
    completed = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return f"{self.title} - Lesson {self.lesson_number} of {self.course.title}"


class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='course_materials', on_delete=models.CASCADE)
    material_file = models.FileField(upload_to='course_materials/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course.title} - Material"

class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    payment_confirmed = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.title} - {self.time_slot}"


class ScheduledClass(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='scheduled_classes')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.schedule.course.title} on {self.schedule.time_slot}"

class DiscountCode(models.Model):
    code = models.CharField(max_length=50)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.code

class Pricing(models.Model):
    course_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.course_type}: {self.price}"

class Homework(models.Model):  # Ensure this class is defined
    file = models.FileField(upload_to='homework/')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Homework for {self.student.user.username} in {self.course.title}"


class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    score = models.IntegerField()  # Define the scoring range, e.g., 1-5
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.username} rated {self.course.title} - {self.score}"

