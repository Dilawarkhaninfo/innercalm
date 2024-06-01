from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('counselors/', views.counselors, name='counselors'),
    path('indcounseling/', views.indcounseling, name='indcounseling'),
    path('gtsessions/', views.gtsessions, name='gtsessions'),
    path('onlinecounseling/', views.onlinecounseling, name='onlinecounseling'),
    path('anxietyquiz/', views.anxietyquiz, name='anxietyquiz'),
    path('contentrecommend/', views.contentrecommend, name='contentrecommend'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),

]
