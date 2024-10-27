from django.contrib import admin
from django.urls import path, include  
from english_school import views 
from django.contrib.auth import views as auth_views
from english_school.views import about_view 

from english_school.views import book_class

from english_school.views import (
    about_view,
    contact_view,
    faq_view,
    policies_view,
    course_detail,
)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('faq/', faq_view, name='faq'),
    path('policies/', policies_view, name='policies'),
    
    # Registration
    path('register/student/', views.register_student, name='register_student'),  # Use views.register_student
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('faq/', faq_view, name='faq'),
    path('policies/', policies_view, name='policies'),

    # Admin Dashboard
    path('admin/', admin.site.urls),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/create-course/', views.create_course, name='create_course'),
    path('admin-dashboard/assign-lesson/', views.assign_lesson, name='assign_lesson'),
    path('admin-dashboard/set-prices/', views.set_course_prices, name='set_course_prices'),
    path('admin-dashboard/manage-schedule/', views.manage_schedule, name='manage_schedule'),
    path('admin-dashboard/create-schedule-slot/', views.create_schedule_slot, name='create_schedule_slot'),
    path('admin-dashboard/create-discount-code/', views.create_discount_code, name='create_discount_code'),
    path('admin/upload-course-materials/', views.upload_materials_view, name='upload_course_materials'),

    # Student Login
    path('student/login/', views.student_login, name='student_login'),  # Use views.student_login
    path('schedule-class/', views.schedule_class, name='schedule_class'),
    path('book-class/', book_class, name='book_class'),

    # Teacher Dashboard
    path('teacher-dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('login/teacher/', views.teacher_login, name='teacher_login'),

    # Student Dashboard
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('select-course/', views.select_course_view, name='select_course'),
    path('book-lesson/', views.book_lesson, name='book_lesson'),

    # Payment URLs
    path('payment/stripe/<int:course_id>/', views.stripe_payment, name='stripe_payment'),
    path('payment/paypal/<int:course_id>/', views.paypal_payment, name='paypal_payment'),
    path('paypal-payment-success/', views.paypal_payment_success, name='paypal_payment_success'),
    path('payment-success/', views.stripe_payment_success, name='stripe_payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),

    # Chat
    path('chat/<str:user_type>/<int:user_id>/', views.private_chat, name='private_chat'),

    # Additional URLs
    path('upload_materials/', views.upload_materials_view, name='upload_materials'),
]
