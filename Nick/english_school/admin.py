from django.contrib import admin
from django.urls import path
from .models import (
    Course, Lesson, Teacher, StudentProfile,
    Enrollment, Schedule, DiscountCode, Pricing, CourseMaterial
)
from .views import upload_materials_view  # Import your view here

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'course_type', 'lessons_count')
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'lesson_number', 'title', 'duration')
    search_fields = ('course__title',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')
    search_fields = ('user__username', 'subject')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age')
    search_fields = ('user__username',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')
    search_fields = ('student__user__username', 'course__title')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'time_slot', 'available')
    search_fields = ('course__title',)

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent')
    search_fields = ('code',)

@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('course_type', 'price')
    search_fields = ('course_type',)

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('course', 'material_file')
    search_fields = ('course__title',)

    # Adding a custom URL for the upload materials view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-course-materials/', self.admin_site.admin_view(upload_materials_view), name='upload_course_materials'),
        ]
        return custom_urls + urls
