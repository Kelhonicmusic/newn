from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
#add
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import StudentLoginForm, StudentRegistrationForm


from .models import Schedule
from .models import ScheduledClass 
from .models import Lesson, Rating
from .forms import RatingForm


import paypalrestsdk
from .forms import (
    StudentRegistrationForm,
    TeacherRegistrationForm,
    CourseForm,
    ScheduleForm,
    DiscountCodeForm,
)
from .models import (
    StudentProfile,
    Teacher,
    Course,
    Schedule,
    DiscountCode,
    Enrollment,
    Pricing,
    Lesson,
)
import stripe
import paypalrestsdk

# Configure PayPal SDK
paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,  # 'sandbox' or 'live'
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET
})

def home_view(request):
    courses = Course.objects.all()  # Fetch all courses from the database
    lesson_times = ['10:00 AM', '12:00 PM', '2:00 PM']  # Example lesson times
    approved_ratings = []  # Fetch approved ratings as needed
    context = {
        'courses': courses,
        'lesson_times': lesson_times,
        'approved_ratings': approved_ratings,
    }
    return render(request, 'english_school/index.html', context)

def about_view(request):
    return render(request, 'english_school/about.html')  # Adjust the template path as necessary

def contact_view(request):
    return render(request, 'english_school/contact.html')  # Adjust the template path as necessary

def faq_view(request):
    return render(request, 'english_school/faq.html')  # Adjust the template path as necessary

def policies_view(request):
    return render(request, 'english_school/policies.html')

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'english_school/course_detail.html', {'course': course})

# Index View
def index(request):
    return render(request, 'english_school/home.html')

#subclass

def schedule_class(request):
    # Your logic to handle class scheduling goes here
    return render(request, 'english_school/schedule_class.html')

def my_classes(request):
    if request.user.is_authenticated and hasattr(request.user, 'studentprofile'):
        scheduled_classes = Schedule.objects.filter(course__studentprofile=request.user.studentprofile)
        return render(request, 'english_school/my_classes.html', {'scheduled_classes': scheduled_classes})
    else:
        return render(request, 'english_school/my_classes.html', {'scheduled_classes': []})

# Helper functions to check user roles
def is_admin(user):
    return user.is_staff

def is_teacher(user):
    return hasattr(user, 'teacher')

def is_student(user):
    return hasattr(user, 'studentprofile')

# Book Lesson View
def book_lesson(request):
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        # Assuming you have a StudentProfile associated with the user
        student_profile = request.user.studentprofile

        # Create enrollment for the student in the selected lesson
        enrollment = Enrollment.objects.create(student=student_profile, lesson=lesson)
        
        # Redirect to a success page or back to lessons
        return redirect('student_dashboard')

    lessons = Lesson.objects.all()  # Adjust as needed to filter lessons
    return render(request, 'english_school/book_lesson.html', {'lessons': lessons})


# Student Registration View
def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and hasattr(user, 'studentprofile'):
                login(request, user)
                return redirect('student_dashboard')  # Redirect to the student dashboard
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = StudentLoginForm()
    return render(request, 'english_school/student_login.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Create a StudentProfile instance if needed
            return redirect('student_login')  # Redirect to login after registration
    else:
        form = StudentRegistrationForm()
    return render(request, 'english_school/register_student.html', {'form': form})


# Teacher Registration View
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Teacher.objects.create(user=user)
            return redirect('teacher_login')  # Redirect to the login page after registration
    else:
        form = TeacherRegistrationForm()
    return render(request, 'english_school/register.html', {'form': form, 'role': 'Teacher'})

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'teacher'):
            login(request, user)
            return redirect('teacher_dashboard')  # Redirect to Teacher Dashboard
        else:
            # Handle login error (e.g., invalid credentials or not a teacher)
            ...
    return render(request, 'english_school/login.html', {'role': 'Teacher'})


# Admin Dashboard View
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    students = StudentProfile.objects.all()
    lessons = Lesson.objects.all()
    schedules = Schedule.objects.all()
    discount_codes = DiscountCode.objects.all()
    pricing = Pricing.objects.first()
    return render(request, 'english_school/admin_dashboard.html', {
        'courses': courses,
        'teachers': teachers,
        'students': students,
        'lessons': lessons,
        'schedules': schedules,
        'discount_codes': discount_codes,
        'pricing': pricing,
    })

# Course Creation View
@login_required
@user_passes_test(is_admin)
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'english_school/create_course.html', {'form': form})

# Assign Lesson to Teacher View
@login_required
@user_passes_test(is_admin)
def assign_lesson(request):
    unassigned_lessons = Lesson.objects.filter(assigned=False)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        teacher_id = request.POST.get('teacher_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        lesson.teacher = teacher
        lesson.assigned = True
        lesson.save()

        # Send email to teacher
        send_mail(
            'New Lesson Assignment',
            f'You have been assigned a new lesson: {lesson.course.title} on {lesson.date_time}.',
            settings.DEFAULT_FROM_EMAIL,
            [teacher.user.email],
            fail_silently=False,
        )

        # Send email to student
        if lesson.student:
            send_mail(
                'Your Lesson is Scheduled',
                f'Your lesson for {lesson.course.title} is scheduled on {lesson.date_time} with {teacher.user.username}.',
                settings.DEFAULT_FROM_EMAIL,
                [lesson.student.user.email],
                fail_silently=False,
            )

        return redirect('admin_dashboard')
    return render(request, 'templates/english_school/assign_lesson.html', {'lessons': unassigned_lessons, 'teachers': teachers})

# Set Course Prices as Ratios
@login_required
@user_passes_test(is_admin)
def set_course_prices(request):
    pricing = Pricing.objects.first()
    if not pricing:
        pricing = Pricing.objects.create()

    if request.method == 'POST':
        pricing.private_ratio = request.POST.get('private_ratio')
        pricing.semi_private_ratio = request.POST.get('semi_private_ratio')
        pricing.group_ratio = request.POST.get('group_ratio')
        pricing.save()

        # Update course prices based on ratios
        Course.objects.filter(course_type=Course.PRIVATE).update(price=pricing.private_ratio)
        Course.objects.filter(course_type=Course.SEMI_PRIVATE).update(price=pricing.semi_private_ratio)
        Course.objects.filter(course_type=Course.GROUP).update(price=pricing.group_ratio)

        return redirect('admin_dashboard')

    return render(request, 'english_school/set_prices.html', {'pricing': pricing})

# Manage Schedule View
@login_required
@user_passes_test(is_admin)
def manage_schedule(request):
    schedules = Schedule.objects.all()
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.available = not schedule.available
        schedule.save()
        return redirect('admin_dashboard')
    return render(request, 'english_school/manage_schedule.html', {'schedules': schedules})

# Create Schedule Slot View
@login_required
@user_passes_test(is_admin)
def create_schedule_slot(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ScheduleForm()
    return render(request, 'english_school/create_schedule_slot.html', {'form': form})

# Upload Materials View (Admin)
@login_required
def upload_materials_view(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect if not admin
    courses = Course.objects.all()
    if request.method == 'POST':
        course_id = request.POST.get('course')
        materials = request.FILES.getlist('materials')  # Get list of uploaded files
        course = get_object_or_404(Course, id=course_id)    
        for material in materials:
            Material.objects.create(course=course, file=material)  # Create Material instance for each file
        messages.success(request, 'Materials uploaded successfully.')
        return redirect('upload_materials')  # Redirect back to upload page

    return render(request, 'english_school/upload_materials.html', {'courses': courses})

# Create Discount Code View
@login_required
@user_passes_test(is_admin)
def create_discount_code(request):
    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.created_by = request.user
            discount.save()
            return redirect('admin_dashboard')
    else:
        form = DiscountCodeForm()
    return render(request, 'english_school/create_discount_code.html', {'form': form})

# Teacher Dashboard View
@login_required
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacher = Teacher.objects.get(user=request.user)

    # Modify this line to filter lessons based on existing fields.
    # If you want to show lessons that are not yet completed, you can do:
    lessons = Lesson.objects.filter(course__teacher=teacher, completed=False)  # Adjusting the filter

    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        goal = request.POST.get('goal')
        lesson = get_object_or_404(Lesson, id=lesson_id, course__teacher=teacher)
        lesson.goal = goal
        lesson.completed = True
        lesson.save()
        return redirect('teacher_dashboard')

    return render(request, 'english_school/teacher_dashboard.html', {'lessons': lessons})


# Student Dashboard View
@login_required
def student_dashboard(request):
    # Get the student's profile
    student_profile = request.user.studentprofile

    # Fetch the student's enrollments
    enrollments = Enrollment.objects.filter(student=student_profile)

    # Check if the student has any enrollments
    if not enrollments.exists():
        # If no enrollments, return a dashboard indicating no courses yet
        return render(request, 'english_school/student_dashboard.html', {
            'message': 'You have not enrolled in any courses yet.',
        })

    # Fetch lessons related to the enrolled courses (if any)
    lessons = Lesson.objects.filter(course__enrollment__student=student_profile, completed=False)

    # Pass the lessons and enrollments to the template
    return render(request, 'english_school/student_dashboard.html', {
        'enrollments': enrollments,
        'lessons': lessons,
    })

# Select Course View
@login_required
@user_passes_test(is_student)
def select_course_view(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        selected_course = get_object_or_404(Course, id=course_id)
        # Logic for course selection
        return redirect('student_dashboard')

    return render(request, 'english_school/select_course.html', {'courses': courses})


# chat private

def private_chat(request, user_type, user_id):
    # Your view logic here
    return render(request, 'chat/private_chat.html', {'user_type': user_type, 'user_id': user_id})

# Payment View
@login_required
@user_passes_test(is_student)
def payment_view(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')
        if payment_method == 'paypal':
            # PayPal payment processing
            pass
        elif payment_method == 'stripe':
            # Stripe payment processing
            pass
    return render(request, 'english_school/payment.html')
    

# API for Stripe Payment
@csrf_exempt
def stripe_payment(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        # Logic for Stripe payment processing
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})

    # indented success function

def stripe_payment_success(request):
    return render(request, 'english_school/stripe_payment.html')

# paypal

@csrf_exempt
def paypal_payment(request, course_id):
    # Get the course by ID
    course = get_object_or_404(Course, id=course_id)

    # Create a PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/success/",
            "cancel_url": "http://localhost:8000/payment/cancel/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": course.title,
                    "sku": course.id,
                    "price": str(course.price),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(course.price),
                "currency": "USD"
            },
            "description": "Payment for course: {}".format(course.title)
        }]
    })

    # Create the payment and redirect the user
    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        print("Error while creating payment: {}".format(payment.error))
        return JsonResponse({"error": "Payment creation failed"}, status=400)

@csrf_exempt
def paypal_payment_success(request):
    return render(request, 'english_school/paypal_payment_success.html')

def payment_cancel(request):
    return render(request, 'english_school/payment_cancel.html')

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def book_class(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    # Check if the student is already booked for this class
    if ScheduledClass.objects.filter(student=request.user, schedule=schedule).exists():
        # Redirect or show a message if the class is already booked
        return render(request, 'english_school/already_booked.html', {'schedule': schedule})
    
    # Create a new ScheduledClass instance if not already booked
    ScheduledClass.objects.create(student=request.user, schedule=schedule)
    
    # Redirect to the my_classes page or a confirmation page
    return redirect('my_classes') 


#Backend Booking logic for the booking added to the front end.
def book_lesson(request):
    if request.method == 'POST' and request.user.is_authenticated:
        course_id = request.POST.get('courseId')
        lesson_date = request.POST.get('lessonDate')

        # Logic to create a scheduled class
        scheduled_class = ScheduledClass.objects.create(
            student=request.user,
            course_id=course_id,
            date=lesson_date,
            # Add any other required fields
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


def index(request):
    # Generate lesson times
    lesson_times = []
    start_time = datetime.strptime("07:00", "%H:%M")
    end_time = datetime.strptime("22:00", "%H:%M")
    
    while start_time < end_time:
        lesson_times.append(start_time.strftime("%I:%M %p"))
        start_time += timedelta(minutes=50)  # 40 minutes lesson + 10 minutes interval

    courses = []  # Replace this with your course fetching logic
    context = {
        'lesson_times': lesson_times,
        'courses': courses,
    }
    return render(request, 'english_school/index.html', context)



def cancel_lesson(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id, student=request.user)
        lesson_start_time = make_aware(datetime.combine(lesson.date, lesson.start_time))
        
        # Check if the lesson is within 24 hours
        if timezone.now() >= lesson_start_time - timedelta(hours=24):
            # You may want to handle this case with a message to the user
            return redirect('student_dashboard')  # Redirect or show a message

        lesson.is_cancelled = True
        lesson.save()
        return redirect('student_dashboard')


def rate_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, student=request.user)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.lesson = lesson
            rating.student = request.user
            rating.save()
            return redirect('student_dashboard')  # Redirect after saving
    else:
        form = RatingForm()
    
    return render(request, 'rate_lesson.html', {'form': form, 'lesson': lesson})


def home(request):
    approved_ratings = Rating.objects.filter(approved=True).order_by('-created_at')[:5]  # Fetch the latest 5 approved ratings
    return render(request, 'index.html', {'approved_ratings': approved_ratings})


def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('course_title')
        description = request.POST.get('course_description')
        course_type = request.POST.get('course_type')
        lessons_count = request.POST.get('lessons_count')
        price = request.POST.get('course_price')
        materials = request.FILES.getlist('materials')  # Get list of uploaded files

        # Create the course
        new_course = Course(
            title=title,
            description=description,
            course_type=course_type,
            lessons_count=lessons_count,
            price=price
        )
        new_course.save()  # Save the course instance

        # Save course materials
        for material in materials:
            CourseMaterial.objects.create(course=new_course, material_file=material)

        messages.success(request, 'Course created successfully!')
        return redirect('admin_dashboard')  # Redirect to admin dashboard or relevant page

    return render(request, 'admin_dashboard.html')









