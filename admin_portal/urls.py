from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('home/', views.admin_home, name='home'),
    path('alluser/', views.all_users, name='alluser'),
    path('allappointments/', views.all_appointments, name='allappointments'),
    path('allcounselors/', views.all_counselors, name='allcounselors'),
    path('addcounselors/', views.add_counselors, name='addcounselors'),
    path('store_counselor/', views.store_counselor, name='store_counselor'),
    path('delete_counselor/<int:id>/', views.delete_counselor, name='delete_counselor'),
    path('allresources/', views.all_resources, name='allresources'),
    path('viewanalytics/', views.view_analytics, name='viewanalytics'),
    path('allreports/', views.all_report, name='allreports'),
    path('settings/', views.view_settings, name='settings'), 
    # Add more URL patterns as needed
    path('form_index', views.home, name='form_index'),
    path('user-post/', views.userPost, name='user-post'),
    path('topic/<int:pk>/', views.postTopic, name='topic-detail'),
    path('search-result/', views.searchView, name='search-result'),
    path('user-dashboard/', views.userDashboard, name='user-dashboard'),
    path('upvote/', views.upvote, name='upvote'),
    path('downvote/', views.downvote, name='downvote'),
    path('blog/', views.blogListView, name='blog'),
    path('article/<slug:slug>/', views.blogDetailView, name='article-detail'),
]
