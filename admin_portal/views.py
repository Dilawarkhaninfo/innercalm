from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from accounts.models import User, Client, Counselor, Resources, Appointments,Author
from accounts.models import *
from django.contrib.auth.hashers import make_password
from .forms import UserPostForm, AnswerForm
from django.template.loader import render_to_string

from .forms import CounselorForm
@login_required
def admin_home(request):
    user_count = User.objects.count()
    appoint_count = Appointments.objects.count()
    res_count=Resources.objects.count()
    return render(request, 'admin_portal/home.html', {'user_count': user_count, 'appoint_count': appoint_count, 'res_count': res_count})
@login_required
def all_users(request):
    users=User.objects.all()
    return render(request, 'admin_portal/alluser.html',{'users':users})
    
@login_required
def all_appointments(request):
    appoint=Appointments.objects.all()
    return render(request, 'admin_portal/allappointments.html',{'appoint':appoint})
@login_required
def all_counselors(request):
    data=User.objects.filter(is_doc=True)
    return render(request, 'admin_portal/allcounselors.html',{'data':data})
@login_required
def add_counselors(request):
    form = CounselorForm()
    return render(request, 'admin_portal/addcounselor.html',{'form': form})

def store_counselor(request):
    if request.method == 'POST':
        form = CounselorForm(request.POST,request.FILES)
        if form.is_valid():
            f_name = form.cleaned_data['fname']
            l_name = form.cleaned_data['lname']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            qual = form.cleaned_data['qual']
            spec = form.cleaned_data['spec']
            location = form.cleaned_data['location']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            image = form.cleaned_data['image']
            is_doc=True
            user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_doc=True
            )
            user.save()
            counselor_instance = Counselor.objects.create(
                user=user,
                f_name=f_name,
                l_name=l_name,
                specialization=spec,
                qualification=qual,
                image=image
            )
            counselor_instance.save()
            author_inst=Author.objects.create(
                user=user
            )
            author_inst.save()
    return redirect('admin_portal:home')

def delete_counselor(request, id):
    counselor = get_object_or_404(Counselor, user_id=id) 
    u_id=counselor.user.id
    counselor.delete()
    user = get_object_or_404(User, id=u_id)
    user.delete()
    return redirect('admin_portal:home')    


    

# def store_counselor(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         raw_password = request.POST.get('password')
#         f_name = request.POST.get('f_name')
#         l_name = request.POST.get('l_name')
#         specialization = request.POST.get('spec')
#         qualification = request.POST.get('qual')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         location = request.POST.get('location')
#         age = request.POST.get('age')
#         gender = request.POST.get('gender')
#         password = make_password(raw_password)
#         user = User.objects.create_user(
#             username=username,
#             password=password,
#             email=email,
#             is_doc=True
#         )
#         user.phone = phone
#         user.age = age
#         user.location = location
#         user.gender = gender
#         user.is_active = True
#         user.save()
#         Counselor.objects.create(
#             user=user,
#             f_name=f_name,
#             l_name=l_name,
#             specialization=specialization,
#             qualification=qualification
#         )
#         return render(request, 'admin_portal/addcounselor.html')
#     else:
#         return render(request, 'admin_portal/addcounselor.html')
@login_required
def all_resources(request):
    data=Resources.objects.all()
    return render(request, 'admin_portal/allresources.html',{'data':data})
@login_required
def all_report(request):
    # Add logic here if needed
    return render(request, 'admin_portal/allreport.html')
@login_required
def view_analytics(request):
    # Add logic here if needed
    return render(request, 'admin_portal/viewanalytics.html')
@login_required
def view_settings(request):
    user=request.user
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.location = request.POST.get('location')
        user.age = request.POST.get('age')
        user.lang = request.POST.get('lang')
        user.save()
        return redirect('admin_portal:home')
    return render(request, 'admin_portal/settings.html',{'user':user})

# Form

def home(request):
    user_posts = UserPost.objects.all()
    
    # Display latest posts.
    latest_blogs = BlogPost.objects.order_by('-timestamp')[0:3]

    latest_topics = UserPost.objects.order_by('-date_created')[0:3]
    
    context = {
        'user_posts':user_posts,
        'latest_blogs':latest_blogs,
        'latest_topics':latest_topics
    }
    return render(request, 'form/forum-main.html', context)

@login_required
def userPost(request):
    # User Post form.
    form = UserPostForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            author=request.user.author
            if author:
                title = request.POST.get('title')
                description = request.POST.get('description')
                topic = UserPost.objects.create(title=title, author=request.user.author, description=description)
                topic.save()
                return redirect('admin_portal:form_index')
            else:
                form = UserPostForm()
                context = {'form':form}
                return render(request, 'form/user-post.html', context)
    else:
        form = UserPostForm()

    context = {'form':form}
    return render(request, 'form/user-post.html', context)

@login_required(login_url='login')
def postTopic(request, pk):
    # Get specific user post by id.
    post_topic = get_object_or_404(UserPost, pk=pk)

    # Count Post View only for authenticated users
    if request.user.is_authenticated:
        TopicView.objects.get_or_create(user=request.user, user_post=post_topic)

    # Get all answers of a specific post.
    answers = Answer.objects.filter(user_post = post_topic)

    # Answer form.
    answer_form = AnswerForm(request.POST or None)
    if request.method == "POST":
        if answer_form.is_valid():
            content = request.POST.get('content')
            # passing User Id & User Post Id to DB
            ans = Answer.objects.create(user_post=post_topic, user=request.user, content=content)
            ans.save()
            return HttpResponseRedirect(post_topic.get_absolute_url())
    else:
        answer_form = AnswerForm()
    
    context = {
        'topic':post_topic,
        'answers':answers,
        'answer_form':answer_form,
        
    }
    return render(request, 'form/topic-detail.html', context)

@login_required(login_url='login')
def userDashboard(request):
    topic_posted = request.user.author.userpost_set.all()
    ans_posted = request.user.answer_set.all()
    topic_count = topic_posted.count()
    ans_count = ans_posted.count()
    
    context = {
        'topic_posted':topic_posted,
        'ans_posted':ans_posted,
        'topic_count':topic_count,
        'ans_count':ans_count
    }
    return render(request, 'form/user-dashboard.html', context)

def searchView(request):
    queryset = UserPost.objects.all()
    search_query = request.GET.get('q')

    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query) 
        ).distinct()
        
        q_count = queryset.count()
    else:
        messages.error(request, f"Oops! Looks like you didn't put any keyword. Please try again.")
        return redirect('admin_portal:form_index')

    
    context = {
        'queryset':queryset,
        'search_query':search_query,
        'q_count':q_count
    }

    return render(request, 'form/search-result.html', context)


def upvote(request):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    
    has_upvoted = False

    if answer.upvotes.filter(id = request.user.id).exists():
        answer.upvotes.remove(request.user)
        has_upvoted = False        
    else:
        answer.upvotes.add(request.user)
        answer.downvotes.remove(request.user)
        has_upvoted = True

    return HttpResponseRedirect(answer.user_post.get_absolute_url())
    

def downvote(request):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    
    has_downvoted = False
    
    if answer.downvotes.filter(id = request.user.id).exists():
        answer.downvotes.remove(request.user)
        has_downvoted = False
    else:
        answer.downvotes.add(request.user)
        answer.upvotes.remove(request.user)
        has_downvoted = True
    
    return HttpResponseRedirect(answer.user_post.get_absolute_url())

# Blog listing page view.
def blogListView(request):
    
    # Display all blog posts.
    all_posts = BlogPost.objects.all()
    
    context = {
        'all_posts':all_posts
    }
    return render(request, 'form/blog-listing.html', context)

    
# Blog single post detail view.
def blogDetailView(request, slug):
    # Get specific post by slug.
    post_detail = get_object_or_404(BlogPost, slug=slug)

    context = {
        'post_detail':post_detail,
    }

    return render(request, 'form/blog-detail.html', context)  



