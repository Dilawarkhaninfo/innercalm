# clients_portal/urls.py

from django.urls import path
from . import views

app_name = 'counselors_portal'

urlpatterns = [
    path('home/', views.counselors_home, name='home'),
    path('login/', views.login_view, name='login'),
    path('viewlogin/', views.counselors_viewlogin, name='viewlogin'),
    path('allquiz/', views.all_quiz, name='allquiz'),
    path('allappointments/', views.all_appointments, name='allappointments'),
    path('allfeedback/', views.all_feedback, name='allfeedback'),
    path('addquiz/', views.add_quiz, name='addquiz'),
    path('allresources/', views.all_resources, name='allresources'),
    path('addresources/', views.add_resources, name='addresources'),
    path('settings/', views.view_settings, name='settings'),
    path('edit_appoint/<int:id>', views.edit_appoint, name='edit_appoint'),
    path('api/counselor_appointments/', views.counselor_appointments_data, name='counselor_appointments_data'),
    # Add more URL patterns as needed
]
