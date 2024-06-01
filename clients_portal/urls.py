# clients_portal/urls.py

from django.urls import path
from . import views

app_name = 'clients_portal'

urlpatterns = [
    path('login/', views.clients_login, name='login'),
    path('home/', views.clients_home, name='home'),
    path('viewquiz/', views.view_quiz, name='viewquiz'),
    path('takequiz/', views.take_quiz, name='takequiz'),
    path('takeappointments/', views.take_appointments, name='takeappointments'),
    path('viewappointments/', views.view_appointments, name='viewappointments'),
    path('viewchatbot/', views.chat, name='viewchatbot'),
    path("viewchatbot2", views.chat, name="viewchatbot2"),
    path("ask_question/", views.ask_question, name="ask_question"),
    path("meeting/", views.view_meet, name="meeting"),
    path('viewrecommendations/', views.view_recommendations, name='viewrecommendations'),
    path('allcounselors/', views.all_counselors, name='allcounselors'),
    path('allcounselors/', views.view_payment, name='allcounselors'),
    path('settings/', views.view_settings, name='settings'),
    path('delete_appoint/<int:id>/', views.delete_appoints, name='delete_appoint'),

    # Add more URL patterns as needed
    
    # API
    path('get_user_data/<int:userId>', views.get_user_data, name='get_user_data'),
    path('api/stress_level/', views.stress_level, name='stress_level'),
    path('store_ratings/',views.store_ratings,name='store_ratings'),
    path('api/appointments/', views.appointments_data, name='appointments_data')
]

