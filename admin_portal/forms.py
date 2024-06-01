from django import forms
from accounts.models import User

class CounselorForm(forms.Form):
    fname = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    lname = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    phone = forms.CharField(label='Phone Number', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    qual = forms.CharField(label='Qualifications', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter qualifications'}))
    spec = forms.CharField(label='Specialties', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialties'}))
    location = forms.ChoiceField(label='Location', choices=[('Lahore', 'Lahore'), ('Islamabad', 'Islamabad'), ('Karachi', 'Karachi'), ('Peshawar', 'Peshawar'), ('Quetta', 'Quetta'), ('Rawalpindi', 'Rawalpindi')], widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}))
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female')], widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}))
    age = forms.CharField(label='Age', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}))
    image = forms.ImageField(label='Profile Picture', required=False)

from accounts.models import *

class UserPostForm(forms.ModelForm):

    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class':'form-control form-control-style-3',
        'placeholder':'Title',
    }))

    description = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class':'form-control form-control-style-3',
        'placeholder':'Description in detail...',
        'rows':'8',
        'cols':'80',
    }))

    class Meta:
        model = UserPost
        fields = ['title', 'description']

class AnswerForm(forms.ModelForm):

    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class':'form-control form-control-style-3',
        'placeholder':'Write your answer...',
        'rows':'8',
        'cols':'50',
    }))

    class Meta:
        model = Answer
        fields = ['content',]