from django.shortcuts import render,redirect
from accounts.models import User, Client, Counselor, Resources, Quiz, QuizFilled, Appointments
from innercalm import settings
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth import authenticate, login, logout
from accounts.models import Client, Counselor, User,Author
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.timezone import now

def counselors_home(request):
    appoint=Appointments.objects.filter(counselor=request.user).count()
    appoint_data=Appointments.objects.filter(status='scheduled').count()
    resouce=Resources.objects.filter(user=request.user).count()
    return render(request, 'counselors_portal/home.html',{'appoint':appoint,'appoint_data':appoint_data,'resouce':resouce})


def all_quiz(request):
    data=QuizFilled.objects.all()
    return render(request, 'counselors_portal/allquiz.html',{'data':data})

def all_appointments(request):
    appoint=Appointments.objects.filter(counselor=request.user)
    return render(request, 'counselors_portal/allappointments.html',{'appoint':appoint})

def all_feedback(request):
    # Add logic here if needed
    return render(request, 'counselors_portal/allfeedback.html')

def counselors_viewlogin(request):
    # Add logic here if needed
    return render(request, 'counselors_portal/login.html')

def add_quiz(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        user = request.user
        Quiz.objects.create(question=question, user=user)
        return render(request, 'counselors_portal/addquiz.html')
    return render(request, 'counselors_portal/addquiz.html')

def all_resources(request):
    user=request.user
    data=Resources.objects.filter(user=user)
    return render(request, 'counselors_portal/allresources.html',{'data':data})

def add_resources(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        keywords = request.POST.get('keywords')
        media = request.FILES.get('media')
        media_path = None  

        if media:
            fs = FileSystemStorage()
            filename = fs.save(media.name, media)
            media_path = os.path.join(settings.MEDIA_URL, filename)
        
        link = request.POST.get('link')
        user = request.user
        Resources.objects.create(title=title, description=description, media=media_path, link=link, user=user, keywords=keywords)
        return render(request, 'counselors_portal/addresources.html')
    return render(request, 'counselors_portal/addresources.html')


def view_settings(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.age = request.POST.get('age')
        user.phone = request.POST.get('phone')
        user.location = request.POST.get('location')
        user.lang = request.POST.get('lang')
        
        user.save()
        return redirect('counselors_portal:home')
    user=request.user
    return render(request, 'counselors_portal/settings.html',{'user':user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_portal:home')
            elif user.is_client:
                print(user)
                return redirect('clients_portal:home')
            elif user.is_doc:
                return redirect('counselors_portal:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'counselors_portal/login.html')
    return render(request, 'counselors_portal/login.html')

def edit_appoint(request, id):
    appoint = Appointments.objects.get(id=id)
    if request.method == 'POST':
        appoint.p_name=request.POST.get('p_name')
        base_url="https://meet.jit.si/innercalm/"
        msg=request.POST.get('p_name')
        appoint.meeting_link=base_url+msg
        appoint.p_contact=request.POST.get('p_contact')
        appoint.client=request.user
        appoint.reason=request.POST.get('reason')
        appoint.duration=request.POST.get('duration')
        appoint.type=request.POST.get('a_type')
        appoint.time=request.POST.get('time')
        appoint.date=request.POST.get('date')
        appoint.status='Scheduled'
        appoint.save()
        send_re_email(appoint)
        return redirect('counselors_portal:allappointments')
    else:
        return render(request, 'counselors_portal/editappointments.html', {'appoint': appoint})
    
def send_re_email(appoint):
    subject = 'Appointment Rescheduling Notification'
    message = format_html(
        '''
        <p>Dear {},</p>
        <p>Your appointment has been rescheduled due to conflict issues.Please visit on <strong>{}</strong> at <strong>{}</strong>.</p>
        <p>If this was not you, please contact our support immediately.</p>
        <p>Best regards,</p>
        <p>InnerCalm.com</p>
        ''',appoint.p_name, appoint.date, appoint.time
    )

    send_mail(
        subject,
        message,
        'no-reply@example.com',
        [appoint.p_contact],
        html_message=message,
        fail_silently=False,
    )

from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count

def counselor_appointments_data(request):
    counselor = request.user

    # Query the Appointments model to get the number of appointments grouped by month for the logged-in counselor
    appointments_data = Appointments.objects.filter(counselor=counselor).annotate(month=ExtractMonth('date')).values('month').annotate(appointments_count=Count('id')).order_by('month')

    # Initialize data lists
    labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    appointments_counts = [0] * 12  # Initialize with zero counts for each month

    # Populate data lists with the actual data
    for data in appointments_data:
        month_index = data['month'] - 1  # Convert month to zero-based index
        appointments_counts[month_index] = data['appointments_count']

    # Create the projectData dictionary
    projectData = {
        'labels': labels,
        'datasets': [{
            'label': 'Appointments',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'data': appointments_counts
        }]
    }

    return JsonResponse(projectData)