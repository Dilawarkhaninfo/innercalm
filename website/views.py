from django.shortcuts import render, redirect
from accounts.models import Counselor,Appointments,User


def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')

def counselors(request):
    counselors = Counselor.objects.all()  # Retrieve all counselors from the database

    return render(request, 'website/counselors.html', {'counselors': counselors})

def services(request):
    return render(request, 'website/services.html')
    
def indcounseling(request):
    return render(request, 'website/indcounseling.html')

def gtsessions(request):
    return render(request, 'website/gtsessions.html')

def onlinecounseling(request):
    return render(request, 'website/onlinecounseling.html')

def anxietyquiz(request):
    return render(request, 'website/anxietyquiz.html')

def contentrecommend(request):
    return render(request, 'website/contentrecommend.html')

def portfolio(request):
    return render(request, 'website/portfolio.html')

def contact(request):
    return render(request, 'website/contact.html')




# def take_appointments(request):
#     if request.method=='POST':
#         p_name=request.POST.get('p_name')
#         p_contact=request.POST.get('p_contact')
#         counselor=request.POST.get('counselor')
#         client=request.user
#         user=User.objects.get(id=counselor)
#         reason=request.POST.get('reason')
#         duration=request.POST.get('duration')
#         type=request.POST.get('a_type')
#         time=request.POST.get('time')
#         date=request.POST.get('date')
#         status='Scheduled'
#         Appointments.objects.create(p_name=p_name,p_contact=p_contact,counselor=user,client=client,  reason=reason,duration=duration,type=type,time=time,date=date,status=status)
        
#         return render(request, 'website/home.html')
#     data=User.objects.filter(is_doc=True)
#     return render(request, 'website/home.html',{'data':data})