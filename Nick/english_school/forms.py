# main/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, Teacher, Course, Schedule, DiscountCode, Homework
from .models import Rating 

class StudentLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()  # Add the age field

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'age']

class TeacherRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'course_type', 'lessons_count', 'materials']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['time_slot', 'available']

class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_percent']

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf, .doc, .docx, .mp3'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['course', 'student', 'score', 'comment']