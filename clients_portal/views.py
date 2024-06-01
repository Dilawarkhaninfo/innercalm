from django.shortcuts import render, redirect,reverse
from accounts.models import User,Client,Counselor,Resources,Quiz,QuizFilled,Appointments,ChatBot,Ratings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from keras.models import load_model
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.timezone import now
# model = load_model(r"D:\FYP's 2024\Yusra\backend\innercalm\keras_model.h5")


def clients_login(request):
    # Add logic here if needed
    return render(request, 'clients_portal/login.html')

def clients_home(request):
    user=request.user
    counselor=User.objects.filter(is_doc=True).count()
    appoint=Appointments.objects.filter(client=user.id)
    resouces=Resources.objects.all().count()
    appoint_count=Appointments.objects.filter(client=user).count()
    return render(request, 'clients_portal/home.html',{'counselor':counselor,'appoint':appoint,'resouces':resouces,'appoint_count':appoint_count})

def view_quiz(request):
    user=request.user
    data=QuizFilled.objects.filter(user=user)
    return render(request, 'clients_portal/viewquiz.html',{'data':data})

def view_appointments(request):
    user=request.user
    data=Appointments.objects.filter(client=user)
    return render(request, 'clients_portal/viewappointments.html',{'data':data})

def take_appointments(request):
    if request.method=='POST':
        p_name=request.POST.get('p_name')
        p_contact=request.POST.get('p_contact')
        counselor=request.POST.get('counselor')
        client=request.user
        user=User.objects.get(id=counselor)
        reason=request.POST.get('reason')
        duration=request.POST.get('duration')
        type=request.POST.get('a_type')
        time=request.POST.get('time')
        date=request.POST.get('date')
        status='Scheduled'
        appoint=Appointments.objects.create(p_name=p_name,p_contact=p_contact,counselor=user,client=client, reason=reason,duration=duration,type=type,time=time,date=date,status=status)
        if appoint:
            print(appoint)
            send_book_email(appoint)
        return render(request, 'clients_portal/payment.html')
    else:
        data=User.objects.filter(is_doc=True)
        return render(request, 'clients_portal/takeappointments.html',{'data':data})

def view_meet(request):
    if request.method=='POST':
        base_url="https://meet.jit.si/innercalm/"
        msg=request.POST.get('msg')
        url=base_url+msg
        return redirect(url)
    else:
        return render(request, 'clients_portal/meeting.html')

def take_quiz(request):
    if request.method == 'POST':
        total_score=0
        user = request.user
        for question_id, answer in request.POST.items():
            if question_id.startswith('question'):
                question_id = int(question_id.split('_')[1])
                answer = int(answer)
        
                if question_id in [22, 23, 24, 25, 26, 27, 28, 29, 30]:
                    if answer == 1:
                        total_score += 4
                    elif answer == 2:
                        total_score += 3
                    elif answer == 3:
                        total_score += 2
                    elif answer == 4:
                        total_score += 1
                else:
                    if answer == 1:
                        total_score += 1
                    elif answer == 2:
                        total_score += 2
                    elif answer == 3:
                        total_score += 3
                    elif answer == 4:
                        total_score += 4
                    
                question = Quiz.objects.get(pk=question_id)
                print(total_score)
                total=(total_score-30)/90
                print(total)
                if total < 0.25:
                    answer='Low Stress'
                elif total < 0.5:
                    answer='Moderate Stress'
                elif total < 0.75:
                    answer='High Stress'
                else:
                    answer='Severe Stress'
        response = QuizFilled(user=user,stree_value=total, answer=answer)
        response.save()
        return redirect('clients_portal:viewquiz')
    else:
        quiz_questions = Quiz.objects.all()
        return render(request, 'clients_portal/takequiz.html', {'quiz_questions': quiz_questions})

def view_payment(request):
    if request.method=='POST':
        return render(request, 'clients_portal/payment.html')
    else:
        return redirect('home')

def view_recommendations(request):
    models = Resources.objects.all()
    data_init = list(models)
    random.shuffle(data_init)
    data = data_init[:3]
    return render(request, 'clients_portal/viewrecommendations.html', {'data': data})

def all_counselors(request):
    data=User.objects.filter(is_doc=True)
    return render(request, 'clients_portal/allcounselors.html',{'data':data})



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
        return redirect('clients_portal:home')
    else:
        user=request.user
        return render(request, 'clients_portal/settings.html',{'user':user})


    

# Counselor Data API
def get_user_data(request, userId):
    user = User.objects.get(id=userId)
    counselor = Counselor.objects.get(user=user)

    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': f'{counselor.f_name} {counselor.l_name}',
        'qualification': counselor.qualification,
        'specialization': counselor.specialization,
        'age':user.age,
        'gender':user.gender,
        'lang':user.lang,
        'location':user.location,
        'phone':user.phone,
    }

    return JsonResponse(data)


from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.db.models import Count
from django.db.models import Avg
def stress_level(request):
    # Query the QuizFilled model to get average stress values grouped by month
    stress_data = QuizFilled.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(stress_avg=Avg('stree_value'))

    # Initialize data lists
    labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    stress_values = [0] * 12  # Initialize with zero values for each month

    # Iterate through the queryset to populate data lists
    for data in stress_data:
        month_index = data['month'] - 1  # Convert month to zero-based index
        stress_values[month_index] = data['stress_avg']

    # Create the projectData dictionary
    projectData = {
        'labels': labels,
        'datasets': [{
            'label': 'Stress',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'data': stress_values
        }]
    }

    # Return the data as JSON response
    return JsonResponse(projectData)
def send_book_email(appoint):
    subject = 'Appointment Booking Notification'
    message = format_html(
        '''
        <p>Dear {},</p>
        <p>Your appointment has been booked successfully.Please visit on  <strong>{}</strong> at <strong>{}</strong>.</p>
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

def delete_appoints(request, id):
    appointments = get_object_or_404(Appointments, id=id)
    appointments.delete()
    return redirect('clients_portal:home')   

import google.generativeai as genai
from django.http import HttpResponseRedirect, JsonResponse
import json

genai.configure(api_key="AIzaSyDtJeLR9T2L9P2ZCVO49j9SDWbFquFK_dI")

def ask_question(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("msg")
            if not text:
                return JsonResponse({"error": "Message content must not be empty"}, status=400)
            
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(text)
            
            user = request.user
            ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
            
            response_data = {
                "text": response.text,
            }
            return JsonResponse({"data": response_data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return HttpResponseRedirect(reverse("clients_portal:chat"))
    
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "clients_portal/viewchatbot.html", {"chats": chats})

def store_ratings(request):
    if request.method == 'POST':
        id=request.POST.get('data_id')
        print(id)
        user = User.objects.get(id=29)
        feedback=request.POST.get('feedback')
        date=now()
        Ratings.objects.create(counselor=user,rating=feedback,date=date)
        return redirect('clients_portal:allcounselors')

import datetime
def appointments_data(request):
    current_year = 2024
    appointments = Appointments.objects.filter(date__year=current_year).values('date__month').annotate(count=Count('id'))
    data = {
        "labels": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "data": [0] * 12 
    }
    for appointment in appointments:
        month_index = appointment["date__month"] - 1  
        data["data"][month_index] = appointment["count"]
    
    return JsonResponse(data)