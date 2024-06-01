from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm,RegisterForm
from .models import Client, Counselor, User,Author,ChatBot
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import datetime
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.timezone import now
import google.generativeai as genai
from django.http import HttpResponseRedirect, JsonResponse

genai.configure(api_key="AIzaSyDtJeLR9T2L9P2ZCVO49j9SDWbFquFK_dI")

def ask_question(request):
    if request.method == "POST":
        text = request.POST.get("text")
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        response = chat.send_message(text)
        user = request.user
        ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
        # Extract necessary data from response
        response_data = {
            "text": response.text,  # Assuming response.text contains the relevant response data
            # Add other relevant data from response if needed
        }
        return JsonResponse({"data": response_data})
    else:
        return HttpResponseRedirect(
            reverse("chat")
        )

def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chat_bot.html", {"chats": chats})

def send_login_email(user):
    subject = 'Login Notification'
    login_time = now().strftime('%Y-%m-%d %H:%M:%S')
    message = format_html(
        '''
        <p>Dear {},</p>
        <p>You have successfully logged into the system on <strong>{}</strong>.</p>
        <p>If this was not you, please contact our support immediately.</p>
        <p>Best regards,</p>
        <p>InnerCalm.com</p>
        ''', user.username, login_time
    )

    send_mail(
        subject,
        message,
        'no-reply@example.com',
        [user.email],
        html_message=message,
        fail_silently=False,
    )
def send_signup_email(user):
    subject = 'Login Notification'
    login_time = now().strftime('%Y-%m-%d %H:%M:%S')
    message = format_html(
        '''
        <p>Dear {},</p>
        <p>You have successfully registered into the system on <strong>{}</strong>.</p>
        <p>If this was not you, please contact our support immediately.</p>
        <p>Best regards,</p>
        <p>InnerCalm.com</p>
        ''', user.username, login_time
    )
    send_mail(
        subject,
        message,
        'no-reply@example.com',
        [user.email],
        html_message=message,
        fail_silently=False,
    )

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            send_login_email(user)
            if user.is_superuser:
                return redirect('admin_portal:home')
            elif user.is_client:
                print(user)
                return redirect('clients_portal:home')
            elif user.is_doc:
                return redirect('counselors_portal:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('website:home')


def forgot_view(request):
    return render(request, 'accounts/forgot.html')

def main_view(request):
    return render(request, 'accounts/main.html')

# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         raw_password = request.POST.get('password')
#         email = request.POST.get('email')
#         password = raw_password
#         user = User.objects.create_user(
#             username=username,
#             password=password,
#             email=email,
#             is_client=True
#         )
#         return redirect('accounts:login')
#     else:
#         return render(request, 'accounts/register.html')

def register_view(request):
    if request.method == 'POST':
        print("Ce")
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Ce2")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_client=True
            )
            user.save()
            author_inst=Author.objects.create(
                user=user
            )
            author_inst.save()
            send_signup_email(user)
            return redirect('accounts:login') 
        else:
            print(form.errors)
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})
