from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from .models import Profile
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20,min_length=2)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    username = forms.CharField(max_length=20,min_length=2)
    email = forms.EmailField()
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    cover_img = forms.ImageField(required=False)
    about = forms.CharField(max_length=200,required=False)
    fb = forms.CharField(max_length=100,required=False)
    insta = forms.CharField(max_length=100,required=False)
    linkedin = forms.CharField(max_length=100,required=False)
    twitter = forms.CharField(max_length=100,required=False)
    git = forms.CharField(max_length=100,required=False)
    website = forms.CharField(max_length=100,required=False)
    
        
    class Meta:
        model = Profile
        fields = ['image','cover_img','about', 'fb', 'insta','linkedin','twitter','website']