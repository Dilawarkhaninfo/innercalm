from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_doc = models.BooleanField(default=False)
    age = models.IntegerField(default='0')
    gender = models.CharField(default='NA',max_length=10)
    location = models.CharField(default='NA',max_length=50)
    lang=models.CharField(default='NA',max_length=50)
    phone=models.IntegerField(default='0',max_length=12)
    lang=models.CharField(default='NA',max_length=50)
    # Define ManyToManyField relationships with unique related_names
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_user_groups',  # Unique related_name for groups
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_permissions',  # Unique related_name for permissions    
)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    f_name = models.CharField(max_length=100)
    
class Counselor(models.Model):
    f_name = models.CharField(default='NA',max_length=100)
    l_name = models.CharField(default='NA',max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization=models.CharField(default='NA',max_length=50)
    qualification=models.CharField(default='NA',max_length=50)
    rating=models.FloatField(default=0)
    fees=models.FloatField(default=0)
    image = models.ImageField(default="pro_pic.png", null=True, blank=True)
    
class Resources(models.Model):
    title=models.CharField(default='NA',max_length=100)
    description=models.CharField(default='NA',max_length=1000)
    media=models.CharField(max_length=1000,null=True, blank=True)
    link=models.CharField(max_length=1000,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords=models.CharField(max_length=1000,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Quiz(models.Model):
    question=models.CharField(default='NA',max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class QuizFilled(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer=models.CharField(default='NA',max_length=1000)
    stree_value=models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
class Appointments(models.Model):
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counselor_appointments')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_appointments')
    p_name = models.CharField(default='Unknown', max_length=100)
    p_contact = models.CharField(default='Unknown', max_length=100)
    duration = models.CharField(default='0', max_length=50)
    type=models.CharField(default='NA',max_length=50)
    date = models.DateField()
    time = models.TimeField()
    reason=models.CharField(default='NA',max_length=1000)
    status = models.CharField(default='Scheduled', max_length=50) 
    meeting_link = models.CharField(default='NA', max_length=1000)

# Form

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(default="pro_pic.png", null=True, blank=True)

    def __str__(self):
        return self.user.username
class UserPost(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'pk': self.pk})

    @property
    def answer_count(self):
        return Answer.objects.filter(user_post=self).count()
    
    @property
    def topic_view_count(self):
        return TopicView.objects.filter(user_post=self).count()



class Answer(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvotes')
    downvotes = models.ManyToManyField(User, blank=True, related_name='downvotes')

    def __str__(self):
        return self.user_post.title
    
    @property
    def upvotes_count(self):
        return Answer.objects.filter(user=self).count()

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(default="header.jpg", null=True, blank=True)

    def __str__(self):
        return self.title


class TopicView(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user_post.title
    
class ChatBot(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="GeminiUser", null=True
    )
    text_input = models.CharField(max_length=500)
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.text_input
    
class Ratings(models.Model):
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="CounselorRatings", null=True)
    rating = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.rating
    




