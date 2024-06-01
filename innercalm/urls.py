"""
URL configuration for innercalm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# main urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),  # Include website URLs
    path('accounts/', include('accounts.urls')),  # Include accounts URLs
    path('admin_portal/', include('admin_portal.urls')),
    path('clients_portal/', include('clients_portal.urls')),  # Add a trailing slash here
    path('counselors_portal/', include('counselors_portal.urls')),

]


    # Add URLs for other apps here
    # path('admin-portal/', include('admin_portal.urls')),

